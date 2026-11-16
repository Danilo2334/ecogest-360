from decimal import Decimal, InvalidOperation
from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError
from core.validation import mass, scoped, text, provenance, kg, date_time
from core.errors import Conflict
from compost.models import Process, Input, Output, Measurement, Evidence, Verification
from traceability.models import Lot
from traceability.services import consume


def serialize(p):
    output = Output.objects.filter(process=p).first()
    return {
        "id": p.id,
        "provenance": p.provenance,
        "state": p.state,
        "observations": p.observations,
        "verified": p.verifications.filter(decision="confirmado").exists(),
        "inputs": [
            {"lot": i.movement.lot_id, "kg": kg(i.movement.kg)}
            for i in p.inputs.select_related("movement")
        ],
        "output": kg(output.kg) if output else None,
        "destination": output.destination if output else None,
        "evidence": [
            {
                "id": e.id,
                "receiver": e.receiver,
                "date": e.date.isoformat(),
                "reference": e.reference,
                "description": e.description,
                "file": bool(e.file),
            }
            for e in p.evidences.all()
        ],
        "measurements": [
            {
                "type": x.type,
                "value": str(x.value),
                "unit": x.unit,
                "date": x.date.isoformat(),
            }
            for x in p.measurements.all()
        ],
        "verifications": [
            {
                "decision": v.decision,
                "reason": v.reason,
                "actor": v.actor.username,
                "date": v.created_at.isoformat(),
            }
            for v in p.verifications.select_related("actor")
        ],
    }


def create(m, data):
    p = Process.objects.create(
        institution=m.institution,
        provenance=provenance(data),
        actor=m.user,
        observations=str(data.get("observations", ""))[:2000],
    )
    return serialize(p)


def add_input(m, pk, data):
    p = scoped(Process, m, pk, True)
    if p.state != "en_proceso":
        raise Conflict("Proceso finalizado.")
    lot = scoped(Lot, m, data.get("lot"), True)
    if (
        lot.provenance != p.provenance
        or lot.allocations.exclude(generation__material__category="verde").exists()
    ):
        raise ValidationError("Solo orgánicos de la misma procedencia.")
    movement = consume(m, lot, mass(data), "entrada_compostaje", f"Proceso {p.id}")
    i = Input.objects.create(process=p, movement=movement)
    return {"id": i.id, "process": p.id, "available": kg(lot.available())}


def finalize(m, pk, data):
    p = scoped(Process, m, pk, True)
    if p.state != "en_proceso":
        raise Conflict("Proceso ya finalizado.")
    if not p.inputs.exists():
        raise ValidationError("El proceso no tiene entradas.")
    if provenance(data) != p.provenance:
        raise ValidationError("Procedencia debe conservarse.")
    Output.objects.create(
        institution=m.institution,
        process=p,
        kg=mass(data),
        provenance=p.provenance,
        destination=text(data, "destination", 500),
        actor=m.user,
    )
    p.state = "finalizado"
    p.save(update_fields=["state"])
    return serialize(p)


def evidence(m, pk, data, file=None):
    p = scoped(Process, m, pk, True)
    if p.verifications.filter(decision="confirmado").exists():
        raise Conflict("Evidencia de resultado confirmado es inmutable.")
    reference = str(data.get("reference", "")).strip()
    if not reference and not file:
        raise ValidationError("Documento o referencia verificable requeridos.")
    if len(reference) > 500:
        raise ValidationError("Referencia demasiado larga.")
    try:
        date = parse_date(str(data.get("date", "")))
    except ValueError:
        date = None
    if not date:
        raise ValidationError("Fecha de destino requerida.")
    if file:
        if file.size > 10 * 1024 * 1024:
            raise ValidationError("Máximo 10 MiB.")
        head = file.read(16)
        file.seek(0)
        if not (
            head.startswith(b"%PDF-")
            or head.startswith(b"\x89PNG\r\n\x1a\n")
            or head.startswith(b"\xff\xd8\xff")
        ):
            raise ValidationError("Solo PDF, PNG o JPEG.")
        if not head.startswith(b"%PDF-"):
            from PIL import Image

            try:
                Image.open(file).verify()
                file.seek(0)
            except Exception:
                raise ValidationError("Imagen inválida.")
    e = Evidence.objects.create(
        institution=m.institution,
        process=p,
        receiver=text(data, "receiver"),
        date=date,
        description=text(data, "description", 2000),
        reference=reference,
        actor=m.user,
        file=file or "",
    )
    return {"id": e.id}


def verify(m, pk, data):
    p = scoped(Process, m, pk, True)
    if p.verifications.filter(decision="confirmado").exists():
        raise Conflict("Resultado ya confirmado.")
    decision = data.get("decision")
    if decision not in ["confirmado", "rechazado"]:
        raise ValidationError("Decisión inválida.")
    if decision == "confirmado" and (
        p.state != "finalizado"
        or not p.inputs.exists()
        or not Output.objects.filter(process=p).exists()
        or not p.evidences.exists()
    ):
        raise ValidationError(
            "Falta finalización, pesaje o evidencia verificable de destino."
        )
    Verification.objects.create(
        institution=m.institution,
        process=p,
        actor=m.user,
        decision=decision,
        reason=text(data, "reason", 2000),
    )
    return serialize(p)


def measurement(m, pk, data):
    p = scoped(Process, m, pk, True)
    if p.state != "en_proceso":
        raise Conflict("Proceso finalizado.")
    try:
        v = Decimal(str(data.get("value", "")))
    except InvalidOperation:
        raise ValidationError("Valor inválido.")
    if (
        not v.is_finite()
        or abs(v) >= Decimal("1000000000")
        or v.as_tuple().exponent < -3
    ):
        raise ValidationError("Valor fuera de rango.")
    x = Measurement.objects.create(
        institution=m.institution,
        process=p,
        value=v,
        unit=text(data, "unit", 30),
        type=text(data, "type", 50),
        date=date_time(data),
        actor=m.user,
    )
    return {"id": x.id}
