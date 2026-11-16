from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import json
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from core.validation import text, scoped
from core.errors import Conflict
from organizations.models import Area, Membership
from interventions.models import Plan, Revision, Followup, Evaluation
from reports.selectors import report


def valid_date(value):
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        raise ValidationError("Usa una fecha válida YYYY-MM-DD.")


def member_user(m, value):
    try:
        q = Membership.objects.filter(
            institution=m.institution, user_id=int(value), user__is_active=True
        ).first()
    except (ValueError, TypeError):
        q = None
    if not q:
        raise ValidationError("Responsable activo de la misma institución requerido.")
    return q.user


def target_value(value, indicator):
    try:
        v = Decimal(str(value))
    except InvalidOperation:
        raise ValidationError("Meta numérica inválida.")
    if (
        not v.is_finite()
        or v < 0
        or v >= Decimal("1000000000")
        or v.as_tuple().exponent < -3
        or (indicator == "rate" and v > 100)
    ):
        raise ValidationError("Meta no negativa hasta 3 decimales; tasa entre 0 y 100.")
    return v


def period(filters):
    start, end = valid_date(filters.get("generated_from")), valid_date(
        filters.get("generated_to")
    )
    if start > end or end >= timezone.localdate():
        raise ValidationError("Usa un período cerrado, hasta ayer.")
    return start, end


def snapshot(m, filters, indicator):
    summary, rows = report(m, filters)
    payload = {
        "rows": rows,
        "generated": summary["generated"],
        "verified_compost": summary["verified_compost"],
    }
    return {
        "value": summary[indicator],
        "summary": summary,
        "sources": rows,
        "fingerprint": hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest(),
    }


def state_data(p):
    return dict(
        id=p.pk,
        problem=p.problem,
        action=p.action,
        area=p.area_id,
        responsible=p.responsible_id,
        indicator=p.indicator,
        target=str(p.target),
        direction=p.direction,
        due_date=str(p.due_date),
        filters=p.filters,
        baseline=p.baseline,
        state=p.state,
        version=p.version,
        provenance=p.filters["provenance"],
    )


def serialize(p):
    return {
        **state_data(p),
        "responsible_name": p.responsible.username,
        "area_name": p.area.name,
        "revisions": [
            {
                "id": r.pk,
                "actor": r.actor.username,
                "date": r.created_at.isoformat(),
                "reason": r.reason,
                "before": r.before,
                "after": r.after,
            }
            for r in p.revisions.select_related("actor").order_by("pk")
        ],
        "followups": [
            {
                "id": r.pk,
                "actor": r.actor.username,
                "date": r.created_at.isoformat(),
                "text": r.text,
            }
            for r in p.followups.select_related("actor").order_by("pk")
        ],
        "evaluations": [
            {
                "id": r.pk,
                "actor": r.actor.username,
                "date": r.created_at.isoformat(),
                **r.result,
            }
            for r in p.evaluations.select_related("actor").order_by("pk")
        ],
    }


def revise(m, p, reason, before):
    Revision.objects.create(
        plan=p, actor=m.user, reason=reason, before=before, after=state_data(p)
    )
    return serialize(p)


def create(m, data):
    reason = text(data, "reason", 2000)
    filters = data.get("filters")
    if (
        not isinstance(filters, dict)
        or set(filters)
        - {"generated_from", "generated_to", "provenance", "area", "material"}
        or any(not isinstance(v, str) for v in filters.values())
    ):
        raise ValidationError(
            "Filtros de cohorte inválidos; no se fija corte histórico."
        )
    period(filters)
    if data.get("scenario") is not None:
        from reports.scenarios import preview

        scenario = data["scenario"]
        if (
            not isinstance(scenario, dict)
            or scenario.get("filters") != filters
            or not scenario.get("base_token")
        ):
            raise ValidationError(
                "La propuesta debe corresponder al área y filtros del plan. Recalcula el escenario."
            )
        preview(
            m,
            {
                "filters": filters,
                "hypothesis": scenario.get("hypothesis"),
                "amount": scenario.get("amount"),
                "base_token": scenario.get("base_token"),
            },
        )
    if filters.get("provenance") not in ("medido", "estimado", "simulado"):
        raise ValidationError("Selecciona una procedencia.")
    area = scoped(Area, m, data.get("area"))
    if filters.get("area") != str(area.pk):
        raise ValidationError("El área del plan debe coincidir con el filtro base.")
    indicator = data.get("indicator")
    if indicator not in ("generated", "verified_compost", "rate"):
        raise ValidationError("Indicador inválido.")
    direction = data.get("direction")
    if direction not in ("reduce", "increase"):
        raise ValidationError("Dirección de meta inválida.")
    baseline = snapshot(m, filters, indicator)
    if not baseline["sources"] or baseline["value"] is None:
        raise ValidationError("Sin línea base evaluable.")
    p = Plan.objects.create(
        institution=m.institution,
        creator=m.user,
        problem=text(data, "problem", 2000),
        action=text(data, "action", 2000),
        area=area,
        responsible=member_user(m, data.get("responsible")),
        indicator=indicator,
        target=target_value(data.get("target"), indicator),
        direction=direction,
        due_date=valid_date(data.get("due_date")),
        filters=filters,
        baseline=baseline,
    )
    return revise(m, p, reason, {})


def mutate(m, pk, action, data):
    p = scoped(Plan, m, pk, True)
    if type(data.get("version")) is not int or data["version"] != p.version:
        raise Conflict("El plan cambió. Recarga antes de editar.")
    if p.state in ("cerrado", "cancelado"):
        raise ValidationError("Plan terminal; su historia se conserva sin editar.")
    reason = text(data, "reason", 2000)
    before = state_data(p)
    if action == "edit":
        if set(data) - {
            "version",
            "reason",
            "problem",
            "action",
            "responsible",
            "target",
            "direction",
            "due_date",
        }:
            raise ValidationError(
                "El universo y la base no se sustituyen: crea un plan nuevo."
            )
        for field in ("problem", "action"):
            if field in data:
                setattr(p, field, text(data, field, 2000))
        if "responsible" in data:
            p.responsible = member_user(m, data["responsible"])
        if "target" in data:
            p.target = target_value(data["target"], p.indicator)
        if "direction" in data:
            if data["direction"] not in ("reduce", "increase"):
                raise ValidationError("Dirección inválida.")
            p.direction = data["direction"]
        if "due_date" in data:
            p.due_date = valid_date(data["due_date"])
    elif action == "transitions":
        dest = data.get("state")
        if (
            dest != "cancelado"
            and {
                "borrador": "en_curso",
                "en_curso": "en_evaluacion",
                "en_evaluacion": "cerrado",
            }.get(p.state)
            != dest
        ):
            raise ValidationError("Transición no permitida.")
        if dest == "en_curso":
            member_user(m, p.responsible_id)
            p.baseline = snapshot(m, p.filters, p.indicator)
            if not p.baseline["sources"] or p.baseline["value"] is None:
                raise ValidationError("La base ya no es evaluable.")
        if dest == "cerrado":
            latest = p.evaluations.order_by("-pk").first()
            if not latest or latest.version != p.version:
                raise ValidationError("Evalúa con la versión actual antes de cerrar.")
        p.state = dest
    elif action == "followups":
        Followup.objects.create(plan=p, actor=m.user, text=text(data, "text", 2000))
    elif action == "evaluations":
        if p.state != "en_evaluacion":
            raise ValidationError("Pasa el plan a en evaluación primero.")
        filters = {
            **p.filters,
            "generated_from": data.get("generated_from"),
            "generated_to": data.get("generated_to"),
        }
        start, end = period(filters)
        base_start, base_end = period(p.filters)
        if start <= base_end or end - start != base_end - base_start:
            raise ValidationError(
                "Período posterior separado y de igual duración requerido."
            )
        current = snapshot(m, p.filters, p.indicator)
        after = snapshot(m, filters, p.indicator)
        result = "no_evaluable"
        explanation = "Falta evidencia comparable o la fuente base cambió; no se afirma una mejora."
        if (
            current["fingerprint"] == p.baseline["fingerprint"]
            and after["sources"]
            and after["value"] is not None
        ):
            value = Decimal(after["value"])
            achieved = (
                value <= p.target if p.direction == "reduce" else value >= p.target
            )
            result = "alcanzada" if achieved else "no_alcanzada"
            explanation = "Comparación descriptiva; distinta maduración y cobertura posibles. No prueba causalidad."
        Evaluation.objects.create(
            plan=p,
            actor=m.user,
            version=p.version + 1,
            result={
                "status": result,
                "explanation": explanation,
                "filters": filters,
                "observation": after,
                "target": str(p.target),
                "direction": p.direction,
            },
        )
    else:
        raise ValidationError("Acción inválida.")
    p.version += 1
    p.save()
    return revise(m, p, reason, before)
