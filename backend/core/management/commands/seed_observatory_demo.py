"""Explicit, isolated synthetic cohort. No automatic startup hook or destructive reset."""

import hashlib
import json
import os
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django.utils import timezone
from organizations.models import Institution, Membership, Site, Area
from catalog.models import Material
from waste.models import Generation
from core.models import AuditEvent
from waste import services as waste
from traceability import services as trace
from compost import services as compost

NAME = "DEMO INTELLIGENCE · SIMULADO · v1"
ENTITY = "demo:observatory-v1"
ROLES = ("administrador", "operador", "gestor", "consultor")


def fingerprint(institution):
    # Include domain records and memberships; additions/edits prevent silent repair.
    from django.apps import apps

    payload = {}
    for model in apps.get_models():
        if model is AuditEvent:
            continue
        if any(f.name == "institution" for f in model._meta.fields):
            payload[model._meta.label] = list(
                model.objects.filter(institution=institution).order_by("pk").values()
            )
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode()
    ).hexdigest()


class Command(BaseCommand):
    help = "Cohorte SIMULADA aislada; sin --apply no escribe. Nunca restablece datos."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true")
        parser.add_argument("--describe", action="store_true")
        parser.add_argument("--end-date")

    @transaction.atomic
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_xact_lock(%s)", [360002])
        institution = Institution.objects.filter(name=NAME).first()
        manifest = (
            AuditEvent.objects.filter(institution=institution, entity=ENTITY).first()
            if institution
            else None
        )
        if manifest:
            if (
                options["end_date"]
                and options["end_date"] != manifest.after["current_to"]
            ):
                raise CommandError(
                    "La cohorte existente tiene otro período; no se modifica."
                )
            if fingerprint(institution) != manifest.after["fingerprint"]:
                raise CommandError(
                    "La cohorte cambió después de generarse; no se repara ni duplica."
                )
            self.stdout.write(json.dumps(manifest.after, ensure_ascii=False))
            return
        if options["describe"]:
            raise CommandError("Todavía no existe la cohorte.")
        try:
            end = (
                date.fromisoformat(options["end_date"])
                if options["end_date"]
                else timezone.localdate() - timedelta(days=1)
            )
        except ValueError:
            raise CommandError("Usa fecha ISO YYYY-MM-DD.")
        if end >= timezone.localdate() or end.year < 2000:
            raise CommandError("El período debe finalizar entre 2000 y ayer.")
        result = {
            "version": 1,
            "provenance": "simulado",
            "institution": NAME,
            "current_from": str(end - timedelta(days=13)),
            "current_to": str(end),
            "previous_from": str(end - timedelta(days=27)),
            "previous_to": str(end - timedelta(days=14)),
            "records": 84,
            "users": ["intelligence_" + r for r in ROLES],
        }
        if not options["apply"]:
            self.stdout.write(
                json.dumps({**result, "dry_run": True}, ensure_ascii=False)
            )
            return
        if institution or User.objects.filter(username__in=result["users"]).exists():
            raise CommandError(
                "Colisión de institución o usuario: no se adopta ni modifica contenido existente."
            )
        password = os.getenv("DEMO_PASSWORD", "")
        if len(password) < 12:
            raise CommandError(
                "Configura DEMO_PASSWORD local de al menos 12 caracteres."
            )
        institution = Institution.objects.create(name=NAME)
        members = {}
        for role in ROLES:
            user = User.objects.create_user("intelligence_" + role, password=password)
            members[role] = Membership.objects.create(
                user=user, institution=institution, role=role
            )
        site = Site.objects.create(institution=institution, name="Campus sintético v1")
        areas = [
            Area.objects.create(institution=institution, site=site, name=name)
            for name in ("Cafetería", "Aulas", "Oficinas")
        ]
        materials = [
            Material.objects.create(
                institution=institution, name=name, category=category
            )
            for name, category in [
                ("Orgánicos", "verde"),
                ("Papel y cartón", "blanco"),
                ("No aprovechables", "negro"),
            ]
        ]
        sources = [[], []]
        for n in range(28):
            period, day = divmod(n, 14)
            bases = (8, 5, 3) if period == 0 else (12, 6, 4)
            for i in range(3):
                amount = str(bases[i] + day % 4)
                g = waste.create(
                    members["operador"],
                    {
                        "area": areas[i].pk,
                        "material": materials[i].pk,
                        "kg": amount,
                        "unit": "kg",
                        "provenance": "simulado",
                        "date": f"{end-timedelta(days=27-n)}T10:00:00-05:00",
                        "method": "SIMULADO · escenario sintético reproducible v1; no medición",
                    },
                )
                if i == 0:
                    sources[period].append({"generation": g["id"], "kg": amount})
        for period, (input_kg, output_kg) in enumerate((("60", "19"), ("100", "31"))):
            lot = trace.create(members["operador"], {"sources": sources[period]})
            p = compost.create(
                members["operador"],
                {
                    "provenance": "simulado",
                    "observations": "SIMULADO · sin duración biológica ni calidad certificada",
                },
            )
            compost.add_input(
                members["operador"],
                p["id"],
                {"lot": lot["id"], "kg": input_kg, "unit": "kg"},
            )
            compost.finalize(
                members["operador"],
                p["id"],
                {
                    "kg": output_kg,
                    "unit": "kg",
                    "provenance": "simulado",
                    "destination": "Destino SIMULADO · jardín académico ficticio",
                },
            )
            compost.evidence(
                members["operador"],
                p["id"],
                {
                    "receiver": "Receptor SIMULADO",
                    "date": str(timezone.localdate()),
                    "reference": f"demo:observatory-v1:{period}",
                    "description": "Referencia sintética del escenario; no documento ni evidencia de campo.",
                },
            )
            compost.verify(
                members["gestor"],
                p["id"],
                {
                    "decision": "confirmado",
                    "reason": "Validación SIMULADA por generador del escenario; no realizada por una persona ni certificación ambiental.",
                },
            )
        result["fingerprint"] = fingerprint(institution)
        AuditEvent.objects.create(
            institution=institution,
            actor=members["administrador"].user,
            entity=ENTITY,
            reason="Creación explícita de escenario SIMULADO mediante comando; no actuación humana ambiental.",
            after=result,
        )
        self.stdout.write(json.dumps(result, ensure_ascii=False))
