from django.db.models import Sum
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from core.validation import mass, provenance, date_time, scoped, text, kg
from core.errors import Conflict
from core.models import AuditEvent
from waste.models import Generation
from organizations.models import Area
from catalog.models import Material


def serialize(g):
    assigned = g.allocations.aggregate(v=Sum("kg"))["v"] or 0
    return {
        "id": g.id,
        "area": g.area_id,
        "area_name": g.area.name,
        "material": g.material_id,
        "material_name": g.material.name,
        "category": g.material.category,
        "kg": kg(g.kg),
        "available": kg(g.kg - assigned),
        "date": g.date.isoformat(),
        "provenance": g.provenance,
        "method": g.method,
        "actor": g.actor.username,
        "reviewed": g.reviewed,
    }


def create(m, data):
    area = scoped(Area, m, data.get("area"))
    material = scoped(Material, m, data.get("material"))
    if not material.active or material.category == "especial":
        raise ValidationError("Material no permitido para registro ordinario.")
    origin = provenance(data)
    method = (
        text(data, "method", 500)
        if origin != "simulado"
        else str(data.get("method", ""))[:500]
    )
    g = Generation.objects.create(
        institution=m.institution,
        area=area,
        material=material,
        kg=mass(data),
        date=date_time(data),
        provenance=origin,
        method=method,
        actor=m.user,
    )
    return serialize(g)


def correct(m, pk, data):
    g = scoped(Generation, m, pk, True)
    if g.allocations.exists():
        raise Conflict("La generación ya tiene asignaciones; registra una incidencia.")
    before = serialize(g)
    for key in data:
        if key not in [
            "kg",
            "unit",
            "area",
            "material",
            "date",
            "provenance",
            "method",
            "reason",
        ]:
            raise ValidationError("Campo no corregible.")
    if "kg" in data:
        g.kg = mass(data)
    if "area" in data:
        g.area = scoped(Area, m, data["area"])
    if "material" in data:
        g.material = scoped(Material, m, data["material"])
        if g.material.category == "especial" or not g.material.active:
            raise ValidationError("Material no permitido.")
    if "date" in data:
        g.date = date_time(data)
    if "provenance" in data:
        g.provenance = provenance(data)
    if "method" in data:
        g.method = str(data["method"])[:500]
    if g.provenance != "simulado" and not g.method:
        raise ValidationError("Método requerido.")
    reason = text(data, "reason", 2000)
    g.full_clean()
    g.save()
    after = serialize(g)
    AuditEvent.objects.create(
        institution=m.institution,
        actor=m.user,
        entity=f"generation:{g.pk}",
        reason=reason,
        before=before,
        after=after,
    )
    return after
