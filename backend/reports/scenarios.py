"""Pure hypothetical calculation over current authorized accounting."""

import hashlib
import json
from decimal import Decimal, InvalidOperation
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from core.errors import Conflict
from core.validation import kg
from reports.selectors import report
from waste.models import Generation
from traceability.models import ConsumptionSource


def preview(m, data):
    filters = data.get("filters")
    allowed = {"generated_from", "generated_to", "provenance", "area", "material"}
    if (
        not isinstance(filters, dict)
        or set(filters) - allowed
        or any(not isinstance(v, str) for v in filters.values())
    ):
        raise ValidationError(
            "Usa filtros válidos sin corte histórico: la disponibilidad se consulta ahora."
        )
    if not all(
        filters.get(k) for k in ("generated_from", "generated_to", "provenance")
    ):
        raise ValidationError("Selecciona procedencia y ambas fechas de generación.")
    base, rows = report(m, filters)
    if not rows:
        raise ValidationError(
            "No hay generación para esta cohorte. Revisa los filtros."
        )
    hypothesis = data.get("hypothesis")
    if hypothesis not in ("increase_compost", "reduce_nonrecoverable"):
        raise ValidationError("Elige una de las dos hipótesis disponibles.")
    try:
        amount = Decimal(str(data.get("amount", "")))
    except InvalidOperation:
        raise ValidationError("Cantidad hipotética inválida.")
    if (
        not amount.is_finite()
        or amount < 0
        or amount >= Decimal("1000000000")
        or amount.as_tuple().exponent < -3
    ):
        raise ValidationError(
            "Usa cantidad no negativa, menor a mil millones y hasta tres decimales."
        )
    generations = Generation.objects.filter(
        institution=m.institution, pk__in=[r["id"] for r in rows]
    ).select_related("material")
    consumed = {
        r["allocation__generation_id"]: r["total"]
        for r in ConsumptionSource.objects.filter(
            allocation__generation__in=generations
        )
        .values("allocation__generation_id")
        .annotate(total=Sum("kg"))
    }
    eligible = Decimal(0)
    nonrecoverable = Decimal(0)
    for g in generations:
        if g.material.category == "verde" and g.provenance in ("medido", "simulado"):
            eligible += g.kg - consumed.get(g.pk, Decimal(0))
        if g.material.category == "negro":
            nonrecoverable += g.kg
    token = hashlib.sha256(
        json.dumps(
            {
                "institution": m.institution_id,
                "filters": filters,
                "rows": rows,
                "eligible": kg(eligible),
                "nonrecoverable": kg(nonrecoverable),
                "consumed": {str(k): kg(v) for k, v in consumed.items()},
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()
    if data.get("base_token") is not None and data["base_token"] != token:
        raise Conflict(
            "La base cambió. Recarga y revisa la hipótesis antes de calcular."
        )
    generated, accredited = Decimal(base["generated"]), Decimal(
        base["verified_compost"]
    )
    g, a = generated, accredited
    if hypothesis == "increase_compost":
        if filters["provenance"] == "estimado":
            raise ValidationError(
                "Los estimados no admiten acreditación hipotética. Usa reducción de no aprovechables."
            )
        if amount > eligible:
            raise ValidationError(
                "La hipótesis supera los orgánicos disponibles elegibles."
            )
        a += amount
        formula = "A′ = A + x; G′ = G; pendiente′ = G′ − A′; tasa′ = A′ / G′ × 100"
    else:
        if amount > nonrecoverable:
            raise ValidationError("La reducción supera la generación no aprovechable.")
        g -= amount
        formula = "G′ = G − r; A′ = A; pendiente′ = G′ − A′; tasa′ = A′ / G′ × 100"
    if a > g or eligible < 0:
        raise ValidationError(
            "Base inconsistente; revisa los registros antes de simular."
        )
    rate = format(a / g * 100, ".2f") if g else None
    return {
        "base": base,
        "eligible": kg(eligible),
        "nonrecoverable": kg(nonrecoverable),
        "base_token": token,
        "filters": filters,
        "hypothesis": hypothesis,
        "amount": kg(amount),
        "result": {
            "generated": kg(g),
            "verified_compost": kg(a),
            "pending": kg(g - a),
            "rate": rate,
        },
        "delta": {
            "generated": kg(g - generated),
            "verified_compost": kg(a - accredited),
            "generated_percent": (
                format((g - generated) / generated * 100, ".2f") if generated else None
            ),
            "rate_points": (
                format(Decimal(rate) - Decimal(base["rate"]), ".2f")
                if rate is not None and base["rate"] is not None
                else None
            ),
        },
        "formula": formula,
        "limitations": "ESCENARIO HIPOTÉTICO: no modifica registros, no acredita tratamiento real ni estima salida de compost. Elegibilidad actual, sin reconstrucción histórica. Una reducción de generación no equivale a aprovechamiento.",
    }
