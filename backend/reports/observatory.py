"""Read-only analytical projection. The V1 accounting contract remains authoritative."""

from datetime import timedelta
from decimal import Decimal
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from reports.selectors import report
from waste.models import Generation
from traceability.models import ConsumptionSource
from core.validation import kg


def observatory(m, params):
    filters = dict(params.items())
    filters["cutoff"] = filters.get("cutoff") or timezone.now().isoformat()
    summary, _ = report(m, filters, include_rows=False)  # validates all V1 filters
    cutoff = parse_datetime(summary["cutoff"])
    query = Generation.objects.filter(institution=m.institution)
    for key in ("area", "material", "provenance"):
        if filters.get(key):
            query = query.filter(**{key: filters[key]})
    start = (
        parse_date(filters["generated_from"]) if filters.get("generated_from") else None
    )
    end = parse_date(filters["generated_to"]) if filters.get("generated_to") else None
    if start:
        query = query.filter(date__date__gte=start)
    if end:
        query = query.filter(date__date__lte=end)
    comparison = {
        "available": False,
        "reason": "Selecciona un período completo y una procedencia.",
        "current_from": str(start) if start else None,
        "current_to": str(end) if end else None,
        "previous_from": None,
        "previous_to": None,
        "previous_generated": None,
        "absolute": None,
        "percent": None,
    }
    single = bool(filters.get("provenance"))
    duration = (end - start).days + 1 if start and end else None
    if not single:
        summary["rate"] = None
        comparison["reason"] = (
            "Elige una procedencia: no se combinan mediciones, estimaciones y simulaciones."
        )
    elif start and end:
        if end >= timezone.localdate():
            comparison["reason"] = (
                "El período está abierto. Selecciona fechas hasta ayer para comparar."
            )
        elif duration > 366:
            comparison["reason"] = "La comparación admite hasta 366 días por período."
        elif timezone.localtime(cutoff).date() <= end:
            comparison["reason"] = "El corte debe cubrir el período completo."
        else:
            previous_end = start - timedelta(days=1)
            previous_start = start - timedelta(days=duration)
            previous_filters = {
                **filters,
                "generated_from": str(previous_start),
                "generated_to": str(previous_end),
            }
            previous, _ = report(m, previous_filters, include_rows=False)
            before, current = Decimal(previous["generated"]), Decimal(
                summary["generated"]
            )
            comparison.update(
                previous_from=str(previous_start),
                previous_to=str(previous_end),
                previous_generated=kg(before),
            )
            if before > 0 and query.exists():
                delta = current - before
                comparison.update(
                    available=True,
                    reason="Comparación descriptiva sobre registros vigentes; no prueba causalidad.",
                    absolute=kg(delta),
                    percent=format(delta / before * 100, ".2f"),
                )
            else:
                comparison["reason"] = (
                    "Evidencia insuficiente: falta generación registrada en uno de los períodos."
                )
    series_reason = (
        "Los días omitidos no tienen registros; no representan mediciones de cero kg."
    )
    series = []
    if start and end and duration <= 366:
        series = [
            {"date": str(r["day"]), "kg": kg(r["total"]), "count": r["count"]}
            for r in query.annotate(day=TruncDate("date"))
            .values("day")
            .annotate(total=Sum("kg"), count=Count("id"))
            .order_by("day")
        ]
    else:
        series_reason = "Selecciona ambas fechas, con un máximo de 366 días, para ver la serie diaria."
    accredited = ConsumptionSource.objects.filter(
        allocation__generation__in=query,
        movement__created_at__lte=cutoff,
        movement__compost_input__process__verifications__decision="confirmado",
        movement__compost_input__process__verifications__created_at__lte=cutoff,
        movement__compost_input__process__provenance__in=["medido", "simulado"],
        movement__compost_input__process__provenance=F(
            "allocation__generation__provenance"
        ),
        movement__compost_input__process__output__provenance=F(
            "allocation__generation__provenance"
        ),
    )
    by_area = {
        r["allocation__generation__area_id"]: r["total"]
        for r in accredited.values("allocation__generation__area_id").annotate(
            total=Sum("kg")
        )
    }
    areas = [
        {
            "id": r["area_id"],
            "name": r["area__name"],
            "generated": kg(r["total"]),
            "pending": kg(r["total"] - by_area.get(r["area_id"], Decimal(0))),
        }
        for r in query.values("area_id", "area__name")
        .annotate(total=Sum("kg"))
        .order_by("-total", "area__name", "area_id")
    ]
    origins = [
        {"provenance": r["provenance"], "generated": kg(r["total"])}
        for r in query.values("provenance")
        .annotate(total=Sum("kg"))
        .order_by("provenance")
    ]
    insights = []
    if Decimal(summary["pending"]) > 0:
        insights.append(
            {
                "code": "pending",
                "title": "Hay masa pendiente de acreditación",
                "detail": f"{summary['pending']} kg del universo filtrado aún no tienen compostaje acreditado. Incluye disponibilidad, procesos y entregas.",
                "interpretation": "Pendiente no significa residuo abandonado ni incumplimiento: puede faltar tratamiento o evidencia de destino.",
                "suggestion": "Revisar la cohorte y sus lotes; comprobar disponibilidad, procesos abiertos y evidencias antes de priorizar una intervención.",
            }
        )
    if comparison["available"] and Decimal(comparison["absolute"]) > 0:
        insights.append(
            {
                "code": "increase",
                "title": "Mayor generación registrada",
                "detail": f"{comparison['absolute']} kg más que en el período anterior ({comparison['percent']} %). Revisar los registros antes de concluir una causa.",
                "interpretation": f"La base anterior fue {comparison['previous_generated']} kg, con los mismos filtros. Una diferencia de cobertura también puede cambiar el total.",
                "suggestion": "Contrastar frecuencia de registro y actividad de las áreas en ambos períodos antes de proponer una reducción.",
            }
        )
    if not comparison["available"]:
        insights.append(
            {
                "code": "insufficient",
                "title": "Comparación no disponible",
                "detail": comparison["reason"],
                "interpretation": "La ausencia de registros no prueba ausencia de residuos ni permite evaluar una mejora.",
                "suggestion": "Seleccionar dos períodos completos y revisar la cobertura de la captura de datos.",
            }
        )
    if areas and Decimal(summary["generated"]) > 0:
        top = areas[0]
        share = Decimal(top["generated"]) / Decimal(summary["generated"]) * 100
        insights.append(
            {
                "code": "largest_area",
                "title": f"{top['name']} concentra más generación",
                "detail": f"{top['generated']} kg ({share:.2f} % de la cohorte); {top['pending']} kg pendientes de acreditación.",
                "interpretation": "Es una comparación de masa absoluta, sin normalizar por ocupación ni actividad. No mide eficiencia del área.",
                "suggestion": "Revisar los registros de esta área y su actividad antes de decidir dónde intervenir.",
                "area": top["id"],
            }
        )
    return {
        "summary": summary,
        "comparison": comparison,
        "series": series,
        "areas": areas,
        "provenance_totals": origins,
        "insights": insights,
        "context": {
            "cutoff": summary["cutoff"],
            "coverage": "La ausencia de registros no demuestra ausencia de residuos. Las cohortes tienen distinta maduración; no se reconstruyen correcciones históricas.",
            "series_reason": series_reason,
        },
    }
