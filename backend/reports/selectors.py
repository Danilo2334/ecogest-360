from decimal import Decimal
from django.db.models import Sum, Q, F
from django.utils import timezone
from django.utils.dateparse import parse_datetime, parse_date
from rest_framework.exceptions import ValidationError
from waste.models import Generation
from traceability.models import ConsumptionSource, Allocation
from core.validation import kg


def report(m, params, include_rows=True):
    query = Generation.objects.filter(institution=m.institution).select_related(
        "area", "material", "actor"
    )
    for key, field in [("area", "area_id"), ("material", "material_id")]:
        if params.get(key):
            try:
                query = query.filter(**{field: int(params[key])})
            except ValueError:
                raise ValidationError("Filtro inválido.")
    if params.get("provenance"):
        if params["provenance"] not in ["medido", "estimado", "simulado"]:
            raise ValidationError("Procedencia inválida.")
        query = query.filter(provenance=params["provenance"])
    dates = {}
    for key, field in [
        ("generated_from", "date__date__gte"),
        ("generated_to", "date__date__lte"),
    ]:
        if params.get(key):
            try:
                value = parse_date(params[key])
            except ValueError:
                value = None
            if not value:
                raise ValidationError("Fecha de filtro inválida.")
            dates[key] = value
            query = query.filter(**{field: value})
    if len(dates) == 2 and dates["generated_from"] > dates["generated_to"]:
        raise ValidationError("Intervalo inválido.")
    cutoff = timezone.now()
    if params.get("cutoff"):
        try:
            cutoff = parse_datetime(params["cutoff"])
        except ValueError:
            cutoff = None
        if not cutoff or timezone.is_naive(cutoff):
            raise ValidationError("Corte requiere fecha y zona.")
    generated = query.aggregate(v=Sum("kg"))["v"] or Decimal("0")
    sources = ConsumptionSource.objects.filter(
        allocation__generation__in=query, movement__created_at__lte=cutoff
    )
    filtered_queries = {
        "consumed": sources,
        "delivered": sources.filter(movement__type="entrega"),
        "verified": sources.filter(
            movement__compost_input__process__verifications__decision="confirmado",
            movement__compost_input__process__verifications__created_at__lte=cutoff,
            movement__compost_input__process__provenance__in=["medido", "simulado"],
            movement__compost_input__process__provenance=F(
                "allocation__generation__provenance"
            ),
            movement__compost_input__process__output__provenance=F(
                "allocation__generation__provenance"
            ),
        ),
        "in_process": sources.filter(
            movement__compost_input__process__state="en_proceso"
        ),
    }
    totals = {
        name: q.aggregate(v=Sum("kg"))["v"] or Decimal("0")
        for name, q in filtered_queries.items()
    }
    consumed, delivered, verified, in_process = (
        totals[k] for k in ["consumed", "delivered", "verified", "in_process"]
    )
    distribution = {
        r["material__name"]: r["total"]
        for r in query.values("material__name").annotate(total=Sum("kg"))
    }
    context = {
        "filters": dict(params),
        "cutoff": cutoff.isoformat(),
        "unit": "kg",
        "formula": "Entradas de la cohorte con compostaje validado hasta el corte / generación vigente de la cohorte × 100",
        "limitations": "Solo compostaje acreditado medido o demostración simulada; estimados no acreditables. No representa todo el aprovechamiento institucional. Generación y estados vigentes: no reconstruye correcciones históricas.",
        "provisional": verified < generated,
        "provenance": params.get("provenance", "todas (incluye simulados y estimados)"),
    }
    result = {
        "generated": kg(generated),
        "verified_compost": kg(verified),
        "delivered": kg(delivered),
        "available": kg(generated - consumed),
        "in_process": kg(in_process),
        "pending": kg(generated - verified),
        "rate": format(verified / generated * 100, ".2f") if generated else None,
        "distribution": [
            {"material": name, "kg": kg(value)} for name, value in distribution.items()
        ],
        **context,
    }
    detail = []
    if include_rows:
        accredited = {
            r["allocation__generation_id"]: r["total"]
            for r in filtered_queries["verified"]
            .values("allocation__generation_id")
            .annotate(total=Sum("kg"))
        }
        detail = [
            {
                "id": g.id,
                "date": g.date.isoformat(),
                "area": g.area.name,
                "material": g.material.name,
                "provenance": g.provenance,
                "generated": kg(g.kg),
                "verified_compost": kg(accredited.get(g.id, Decimal("0"))),
            }
            for g in query.order_by("id")
        ]
    return result, detail
