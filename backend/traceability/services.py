from decimal import Decimal
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from core.validation import mass, scoped, text, kg
from core.errors import Conflict
from core.models import AuditEvent
from waste.models import Generation
from traceability.models import Lot, Allocation, Movement, ConsumptionSource


def serialize(lot, detail=False):
    available = lot.available()
    value = {
        "id": lot.id,
        "public_id": str(lot.public_id),
        "provenance": lot.provenance,
        "available": kg(available),
        "state": (
            "cerrado" if lot.closed else ("agotado" if available == 0 else "abierto")
        ),
    }
    if detail:
        value["sources"] = [
            {"generation": a.generation_id, "kg": kg(a.kg)}
            for a in lot.allocations.all()
        ]
        value["movements"] = [
            {
                "id": x.id,
                "type": x.type,
                "kg": kg(x.kg),
                "destination": x.destination,
                "date": x.created_at.isoformat(),
                "actor": x.actor.username,
            }
            for x in lot.movements.select_related("actor").order_by("id")
        ]
    return value


def create(m, data):
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources or len(sources) > 100:
        raise ValidationError("Fuentes requeridas (máximo 100).")
    try:
        ids = [int(s["generation"]) for s in sources]
    except (KeyError, TypeError, ValueError):
        raise ValidationError("Fuentes inválidas.")
    if len(set(ids)) != len(ids):
        raise ValidationError("No repetir origen.")
    locked = {}
    for gid in sorted(ids):
        locked[gid] = scoped(Generation, m, gid, True)
    generations = list(locked.values())
    if (
        len({g.provenance for g in generations}) != 1
        or len({g.material_id for g in generations}) != 1
    ):
        raise ValidationError("El lote requiere mismo material y procedencia.")
    lot = Lot.objects.create(
        institution=m.institution, provenance=generations[0].provenance
    )
    for source in sources:
        g = locked[int(source["generation"])]
        amount = mass({"kg": source.get("kg"), "unit": "kg"})
        assigned = g.allocations.aggregate(v=Sum("kg"))["v"] or Decimal("0")
        if amount > g.kg - assigned:
            raise Conflict("Saldo de generación insuficiente.")
        Allocation.objects.create(generation=g, lot=lot, kg=amount)
    return serialize(lot)


def consume(m, lot, amount, kind, destination):
    if lot.closed:
        raise Conflict("Lote cerrado.")
    if amount > lot.available():
        raise Conflict("Saldo insuficiente.")
    movement = Movement.objects.create(
        institution=m.institution,
        lot=lot,
        kg=amount,
        type=kind,
        destination=destination,
        actor=m.user,
    )
    if kind != "logistico":
        remaining = amount
        for allocation in lot.allocations.select_related("generation").order_by(
            "generation__date", "generation_id"
        ):
            used = allocation.consumptions.aggregate(v=Sum("kg"))["v"] or Decimal("0")
            take = min(remaining, allocation.kg - used)
            if take > 0:
                ConsumptionSource.objects.create(
                    movement=movement, allocation=allocation, kg=take
                )
            remaining -= take
            if remaining == 0:
                break
        if remaining != 0:
            raise Conflict("Distribución de origen inconsistente.")
    return movement


def move(m, pk, data):
    lot = scoped(Lot, m, pk, True)
    kind = data.get("type")
    if kind not in ["logistico", "entrega"]:
        raise ValidationError("Tipo de movimiento inválido.")
    movement = consume(m, lot, mass(data), kind, text(data, "destination", 500))
    return {"id": movement.id, "lot": lot.id, "available": kg(lot.available())}


def close(m, pk):
    from compost.models import Input

    lot = scoped(Lot, m, pk, True)
    if lot.closed:
        raise Conflict("Lote ya cerrado.")
    if (
        lot.available() != 0
        or Input.objects.filter(movement__lot=lot, process__state="en_proceso").exists()
    ):
        raise Conflict("Requiere saldo cero y procesos finalizados.")
    lot.closed = True
    lot.save(update_fields=["closed"])
    AuditEvent.objects.create(
        institution=m.institution,
        actor=m.user,
        entity=f"lot:{lot.id}",
        reason="Cierre",
        after={"closed": True},
    )
    return serialize(lot)
