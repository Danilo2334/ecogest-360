"""Institutional read projection; no new accounting or inferred timestamps."""

from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from core.validation import kg
from core.models import AuditEvent
from traceability.models import Lot
from traceability.services import serialize
from compost.models import Process


def passport(m, uuid):
    lot = get_object_or_404(Lot, institution=m.institution, public_id=uuid)
    events, sources, processes = [], [], []

    def event(
        key,
        kind,
        date,
        actor=None,
        amount=None,
        effect=Decimal(0),
        description="",
        process=None,
        evidence_url=None,
    ):
        events.append(
            dict(
                key=key,
                kind=kind,
                date=date.isoformat(),
                actor=actor,
                kg=kg(amount) if amount is not None else None,
                balance_effect=kg(effect),
                description=description,
                process=process,
                evidence_url=evidence_url,
            )
        )

    assigned = Decimal(0)
    for a in lot.allocations.select_related(
        "generation__area", "generation__material", "generation__actor"
    ).order_by("pk"):
        g = a.generation
        assigned += a.kg
        sources.append(
            dict(
                generation=g.pk,
                area=g.area.name,
                material=g.material.name,
                assigned=kg(a.kg),
                generated=kg(g.kg),
                date=g.date.isoformat(),
                provenance=g.provenance,
            )
        )
        event(
            f"g:{g.pk}",
            "generacion",
            g.date,
            g.actor.username,
            g.kg,
            description=f"{g.material.name} · {g.area.name}. Asignado a este lote: {kg(a.kg)} kg; generación vigente, no nuevo ingreso al saldo.",
        )
        for audit in AuditEvent.objects.filter(
            institution=m.institution, entity=f"generation:{g.pk}"
        ).select_related("actor"):
            event(
                f"audit:{audit.pk}",
                "revision",
                audit.created_at,
                audit.actor.username,
                description=audit.reason,
            )
    event(
        f"l:{lot.pk}",
        "lote",
        lot.created_at,
        amount=assigned,
        effect=assigned,
        description="Creación del lote. El modelo original no conserva autor de esta operación; no se infiere del operador de origen.",
    )
    for move in (
        lot.movements.filter(institution=m.institution)
        .select_related("actor")
        .order_by("created_at", "pk")
    ):
        event(
            f"m:{move.pk}",
            move.type,
            move.created_at,
            move.actor.username,
            move.kg,
            -move.kg if move.type != "logistico" else Decimal(0),
            move.destination,
        )
    for p in Process.objects.filter(
        institution=m.institution, inputs__movement__lot=lot
    ).distinct():
        total = p.inputs.aggregate(v=Sum("movement__kg"))["v"] or Decimal(0)
        own = p.inputs.filter(movement__lot=lot).aggregate(v=Sum("movement__kg"))[
            "v"
        ] or Decimal(0)
        output = getattr(p, "output", None)
        processes.append(
            dict(
                id=p.pk,
                state=p.state,
                provenance=p.provenance,
                lot_input=kg(own),
                total_input=kg(total),
                output=kg(output.kg) if output else None,
                shared=p.inputs.exclude(movement__lot=lot).exists(),
                verified=p.verifications.filter(
                    decision="confirmado", institution=m.institution
                ).exists(),
            )
        )
        for c in p.measurements.filter(institution=m.institution).select_related(
            "actor"
        ):
            event(
                f"control:{c.pk}",
                "control",
                c.date,
                c.actor.username,
                description=f"{c.type}: {c.value} {c.unit}",
                process=p.pk,
            )
        if output and output.institution_id == m.institution_id:
            event(
                f"output:{output.pk}",
                "salida",
                output.created_at,
                output.actor.username,
                output.kg,
                description=f"Salida independiente del proceso completo #{p.pk}; no atribuida como masa propia de este lote. Destino: {output.destination}",
                process=p.pk,
            )
        for e in p.evidences.filter(institution=m.institution).select_related("actor"):
            event(
                f"evidence:{e.pk}",
                "evidencia",
                e.created_at,
                e.actor.username,
                description=f"Destino registrado: {e.date}. {e.reference} · {e.description}",
                process=p.pk,
                evidence_url=f"/api/evidence/{e.pk}/download" if e.file else None,
            )
        for v in p.verifications.filter(institution=m.institution).select_related(
            "actor"
        ):
            event(
                f"verification:{v.pk}",
                "validacion",
                v.created_at,
                v.actor.username,
                description=f"{v.decision}: {v.reason}",
                process=p.pk,
            )
    for a in AuditEvent.objects.filter(
        institution=m.institution, entity=f"lot:{lot.pk}"
    ).select_related("actor"):
        event(
            f"audit:{a.pk}",
            "revision",
            a.created_at,
            a.actor.username,
            description=a.reason,
        )
    events.sort(key=lambda e: (parse_datetime(e["date"]), e["key"]))
    available = lot.available()
    return dict(
        lot=serialize(lot),
        balance=dict(
            assigned=kg(assigned),
            available=kg(available),
            consumed=kg(assigned - available),
        ),
        sources=sources,
        events=events,
        processes=processes,
        cutoff=timezone.now().isoformat(),
        limitations="Historia completa del lote, no limitada al filtro de generación. Traslados no consumen; entrega no acredita; salida de proceso no se suma a entrada. No es certificado ambiental.",
    )
