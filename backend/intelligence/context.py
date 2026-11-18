"""Read-only, institutional projection. Provider never sees free-form database text."""

from collections import defaultdict
from decimal import Decimal
from rest_framework.exceptions import ValidationError
from reports.selectors import report
from traceability.models import Lot

EXPLANATIONS = {
    "rate": "La tasa divide la entrada de residuos de esta cohorte con compostaje validado entre su generación. No mide todo el aprovechamiento institucional.",
    "output": "La entrada es residuo tratado y la salida es otro producto medido de forma independiente. Sumarlas contaría dos veces parte del mismo material; no se presupone rendimiento ni calidad.",
    "provenance": "Medido proviene de una medición; estimado usa un método declarado; simulado sirve para demostración. Un estimado no acredita aprovechamiento efectivo.",
    "pending": "Pendiente significa masa aún no acreditada por este indicador. Puede estar disponible, en proceso o entregada; no demuestra por sí sola una mala gestión.",
    "comparison": "Una diferencia entre períodos describe un cambio, no demuestra su causa. Compara duración, procedencia y maduración de evidencias antes de decidir.",
    "safety": "No se certifica cumplimiento ni calidad del compost. Para residuos peligrosos o especiales consulta el protocolo institucional y al profesional responsable.",
}
ACTIONS = {
    "review": {
        "text": "Revisar registros y evidencias antes de atribuir una causa.",
        "page": "Registros",
    },
    "simulate": {
        "text": "Explorar una hipótesis sin modificar registros ambientales.",
        "page": "Simulador",
    },
    "plan": {
        "text": "Revisar los planes; un gestor decide si crea o modifica un compromiso.",
        "page": "Planes de acción",
    },
}


def build(m, filters):
    allowed = {
        "generated_from",
        "generated_to",
        "area",
        "material",
        "provenance",
        "cutoff",
    }
    if (
        not isinstance(filters, dict)
        or set(filters) - allowed
        or any(not isinstance(v, str) for v in filters.values())
    ):
        raise ValidationError("Filtros no permitidos.")
    if filters.get("provenance") not in ("medido", "estimado", "simulado") or not all(
        filters.get(x) for x in ("generated_from", "generated_to")
    ):
        raise ValidationError(
            "Selecciona un período y una sola procedencia para consultar al asistente."
        )
    summary, rows = report(m, filters)
    metadata = {
        k: summary[k]
        for k in ("filters", "cutoff", "provenance", "unit", "formula", "limitations")
    }
    values = {
        k: summary[k] for k in ("generated", "verified_compost", "pending", "rate")
    }
    facts = [
        {
            "id": "cohort",
            "title": "Balance de la cohorte seleccionada",
            "values": values,
            "page": "Resumen",
        }
    ]
    # Labels remain in local UI; only integer identifiers go to the external provider.
    totals = defaultdict(lambda: Decimal("0"))
    from waste.models import Generation

    generation_ids = [r["id"] for r in rows]
    for g in Generation.objects.filter(
        institution=m.institution, pk__in=generation_ids
    ).select_related("area"):
        totals[(g.area_id, g.area.name)] += g.kg
    for (area_id, name), mass in sorted(totals.items(), key=lambda x: (-x[1], x[0][0]))[
        :3
    ]:
        facts.append(
            {
                "id": f"area:{area_id}",
                "title": name,
                "values": {"generated": format(mass, ".3f")},
                "page": "Registros",
                "area": str(area_id),
            }
        )
    lots = (
        Lot.objects.filter(
            institution=m.institution, allocations__generation_id__in=generation_ids
        )
        .distinct()
        .order_by("pk")
    )
    # A bounded sample, explicitly described as such, never presented as a total.
    from compost.models import Process, Verification

    confirmed = Verification.objects.filter(
        institution=m.institution,
        decision="confirmado",
        created_at__lte=summary["cutoff"],
    ).values("process_id")
    unverified = Process.objects.filter(institution=m.institution).exclude(
        pk__in=confirmed
    )
    for lot in lots.filter(
        movements__compost_input__process__in=unverified,
        movements__created_at__lte=summary["cutoff"],
    ).distinct()[:5]:
        facts.append(
            {
                "id": f"lot:{lot.pk}",
                "title": f"Lote {lot.pk}: revisar proceso sin validación",
                "values": {},
                "page": "Lotes",
                "uuid": str(lot.public_id),
            }
        )
    external = {
        **metadata,
        "facts": [{k: v for k, v in f.items() if k in ("id", "values")} for f in facts],
        "area_ranking": "Hasta tres áreas, ordenadas por masa generada descendente. No normaliza ocupación.",
        "lots": "Muestra de hasta cinco lotes con proceso en curso o finalizado, no es un conteo total.",
        "has_data": bool(rows),
    }
    return {
        "context": metadata,
        "facts": facts,
        "explanations": EXPLANATIONS,
        "actions": ACTIONS,
        "has_data": bool(rows),
    }, external
