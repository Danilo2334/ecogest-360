import json
import re
import uuid
from datetime import timedelta
from decimal import Decimal, InvalidOperation
from django.conf import settings
from django.db import transaction, connection
from django.db.models import Sum
from django.utils import timezone
from rest_framework.exceptions import ValidationError, Throttled
from core.errors import Conflict
from core.validation import text
from intelligence.models import Invocation
from intelligence.context import build
from intelligence import provider

# Explicit allowlist binds model to reviewed prices; no silent price/model fallback.
PRICES = {"gpt-5.6-terra": (Decimal("2.5"), Decimal("12"))}
MAX_INPUT = (
    17024  # <=16000 UTF-8 bytes including schema + conservative framing allowance
)
MAX_OUTPUT = 1000


def configuration():
    try:
        daily, total = (
            Decimal(str(getattr(settings, k, "0")))
            for k in ("AI_DAILY_BUDGET_USD", "AI_PROJECT_BUDGET_USD")
        )
        valid = all(x.is_finite() and x > 0 for x in (daily, total))
    except InvalidOperation:
        return None
    if not (
        settings.AI_ENABLED
        and settings.AI_BUDGET_AUTHORIZED
        and settings.OPENAI_SMOKE_TEST
        and settings.OPENAI_API_KEY
        and settings.OPENAI_MODEL in PRICES
        and valid
    ):
        return None
    return daily, total


def local_context(m, filters):
    local, _ = build(m, filters)
    return dict(
        local,
        status="disponible" if configuration() else "no_disponible",
        reason=(
            ""
            if configuration()
            else "OpenAI está deshabilitado: falta habilitación y presupuesto autorizado. Puedes consultar la explicación local."
        ),
        answer=None,
    )


def reserve(m, key, budgets):
    try:
        key = uuid.UUID(str(key))
    except (ValueError, TypeError, AttributeError):
        raise ValidationError("Identificador de consulta inválido.")
    price_in, price_out = PRICES[settings.OPENAI_MODEL]
    debit = (MAX_INPUT * price_in + MAX_OUTPUT * price_out) / Decimal("1000000")
    now = timezone.now()
    with transaction.atomic():
        # Serializes budget allocation across all web workers and institutions in this app.
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_xact_lock(%s)", [360202602])
        if Invocation.objects.filter(user=m.user, key=key).exists():
            raise Conflict(
                "Consulta ya enviada. No se repetirá el cargo; prepara una nueva consulta."
            )
        if Invocation.objects.filter(user=m.user, status="pending").exists():
            raise Throttled(detail="Ya hay una consulta en curso. Espera su resultado.")
        if (
            Invocation.objects.filter(
                user=m.user, created_at__gte=now - timedelta(minutes=1)
            ).count()
            >= 5
        ):
            raise Throttled(detail="Máximo cinco consultas por minuto.")

        def spent(q):
            return q.aggregate(total=Sum("debit"))["total"] or Decimal("0")

        all_calls = Invocation.objects.all()
        if (
            spent(all_calls) + debit > budgets[1]
            or spent(
                all_calls.filter(institution=m.institution, day=timezone.localdate())
            )
            + debit
            > budgets[0]
        ):
            raise Throttled(
                detail="Presupuesto disponible insuficiente. La consulta no se envió."
            )
        return Invocation.objects.create(
            institution=m.institution,
            user=m.user,
            key=key,
            day=timezone.localdate(),
            model=settings.OPENAI_MODEL,
            debit=debit,
        )


def finish(call, response):
    usage = getattr(response, "usage", None)
    incoming, outgoing = getattr(usage, "input_tokens", None), getattr(
        usage, "output_tokens", None
    )
    if all(isinstance(x, int) and x >= 0 for x in (incoming, outgoing)):
        price_in, price_out = PRICES[call.model]
        call.debit = (incoming * price_in + outgoing * price_out) / Decimal("1000000")
        call.input_tokens, call.output_tokens = incoming, outgoing
        call.status = "completed"
    else:
        call.status = "unknown"  # retain reservation when billing cannot be reconciled
    call.save(update_fields=["debit", "input_tokens", "output_tokens", "status"])


def ask(m, data, key):
    if set(data) - {"mode", "question", "filters"} or data.get("mode") not in (
        "mis_datos",
        "explicar",
        "proponer",
    ):
        raise ValidationError("Consulta o modo no permitido.")
    question = text(data, "question", 2000)
    if re.search(
        r"@|\bsk[-_]|\bgh[pousr]_|-----BEGIN|\b(?:password|contraseña|api[_ -]?key)\s*[:=]|\b\d{7,}\b",
        question,
        re.I,
    ):
        raise ValidationError(
            "No incluyas claves, correos ni datos personales en la pregunta."
        )
    local, external = build(m, data.get("filters"))
    result = dict(local, status="no_disponible", reason="", answer=None)
    budgets = configuration()
    if not budgets:
        result["reason"] = (
            "OpenAI está deshabilitado: falta habilitación y presupuesto autorizado. La información local sigue disponible."
        )
        return result
    if not local["has_data"] and data["mode"] != "explicar":
        result.update(
            status="sin_datos",
            reason="No hay registros de esta cohorte. Ajusta los filtros.",
        )
        return result
    messages = provider.payload(
        data["mode"], question, external, local["explanations"], local["actions"]
    )
    if (
        len(json.dumps(external, ensure_ascii=False).encode()) > 6000
        or len(
            (
                json.dumps(messages, ensure_ascii=False)
                + json.dumps(provider.Selection.model_json_schema())
            ).encode()
        )
        > 16000
    ):
        raise ValidationError(
            "Contexto demasiado amplio. Reduce el período o selecciona un área."
        )
    call = reserve(m, key, budgets)
    response = None
    try:
        response = provider.respond(
            settings.OPENAI_API_KEY, settings.OPENAI_MODEL, messages
        )
        selection = provider.Selection.model_validate(response.output_parsed)
        valid_ids = {f["id"] for f in local["facts"]}
        if response.status != "completed" or not set(selection.sources) <= valid_ids:
            raise ValueError("Unverified response")
        if not selection.insufficient and not (
            selection.sources or selection.explanations
        ):
            raise ValueError("Empty response")
        result.update(status="disponible", answer=selection.model_dump())
    except Exception:
        # Provider errors can embed request text. Do not log, serialize or echo them.
        result["reason"] = (
            "No se obtuvo una respuesta verificable. Consulta las fuentes locales o intenta una nueva consulta más tarde."
        )
    finally:
        finish(call, response)
    return result
