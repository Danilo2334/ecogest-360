import uuid
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from organizations.models import Institution, Membership, Site, Area
from catalog.models import Material
from core.models import AuditEvent, Incident
from waste.models import Generation
from traceability.models import Movement
from django.utils import timezone
from tests.fixtures import Fixture
from django.test import TestCase


class SecurityTests(Fixture, TestCase):
    def test_cross_organization(self):
        other = Institution.objects.create(name="Otra institución fixture")
        site = Site.objects.create(institution=other, name="Otra")
        area = Area.objects.create(institution=other, site=site, name="Otra")
        material = Material.objects.create(
            institution=other, name="Orgánico ajeno", category="verde"
        )
        g = Generation.objects.create(
            institution=other,
            area=area,
            material=material,
            kg=3,
            date=timezone.now(),
            provenance="medido",
            method="Báscula",
            actor=self.operator,
        )
        self.assertEqual(self.client.get(f"/api/generations/{g.id}").status_code, 404)
        self.assertEqual(
            self.post(
                "lots", {"sources": [{"generation": g.id, "kg": "1"}]}
            ).status_code,
            404,
        )
        self.assertEqual(self.client.get("/api/generations").data, [])
        self.assertEqual(self.client.get("/api/dashboard").data["generated"], "0.000")
        self.assertNotIn(
            "Orgánico ajeno",
            self.client.get("/api/reports/generation.csv").content.decode("utf-8"),
        )

    def test_csrf_login_and_logout(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertEqual(
            client.post(
                "/api/session/login",
                {"username": "operador", "password": "Test-only-pass-123!"},
                format="json",
            ).status_code,
            403,
        )
        token = client.get("/api/session/csrf").json()["csrfToken"]
        self.assertEqual(
            client.post(
                "/api/session/login",
                {"username": "operador", "password": "Test-only-pass-123!"},
                format="json",
                HTTP_X_CSRFTOKEN=token,
            ).status_code,
            200,
        )
        self.assertEqual(client.get("/api/session/me").status_code, 200)
        self.assertEqual(
            client.post("/api/session/logout", {}, format="json").status_code, 403
        )
        token = client.get("/api/session/csrf").json()["csrfToken"]
        self.assertEqual(
            client.post(
                "/api/session/logout", {}, format="json", HTTP_X_CSRFTOKEN=token
            ).status_code,
            200,
        )
        self.assertEqual(client.get("/api/session/me").status_code, 401)

    def test_correction_audited_and_incident(self):
        g = self.generation()
        self.client.force_authenticate(self.manager)
        result = self.post(
            f"generations/{g}/correct",
            {"kg": "24", "unit": "kg", "reason": "Transcripción"},
        )
        self.assertEqual(result.status_code, 201, result.data)
        audit = AuditEvent.objects.get(entity=f"generation:{g}")
        self.assertEqual(audit.before["kg"], "25.000")
        self.assertEqual(audit.after["kg"], "24.000")
        self.assertEqual(
            self.post(
                "incidents",
                {"entity": f"generation:{g}", "reason": "Revisar documento"},
            ).status_code,
            201,
        )
        self.assertEqual(Generation.objects.get(pk=g).kg, 24)
        self.client.force_authenticate(self.reader)
        self.assertEqual(
            self.post(
                "incidents", {"entity": f"generation:{g}", "reason": "Intento"}
            ).status_code,
            403,
        )

    def test_idempotency_conflict_and_rollback(self):
        lot, _ = self.lot()
        data = {"kg": "5", "unit": "kg", "type": "entrega", "destination": "Gestor"}
        self.assertEqual(
            self.post(f"lots/{lot}/movements", data, "stable-key").status_code, 201
        )
        self.assertEqual(
            self.post(
                f"lots/{lot}/movements", {**data, "kg": "4"}, "stable-key"
            ).status_code,
            409,
        )
        self.assertEqual(Movement.objects.count(), 1)
        from unittest.mock import patch

        with patch(
            "traceability.services.ConsumptionSource.objects.create",
            side_effect=RuntimeError("injected"),
        ):
            with self.assertRaises(RuntimeError):
                self.post(f"lots/{lot}/movements", data)
        self.assertEqual(Movement.objects.count(), 1)
        self.assertEqual(
            self.client.get(f"/api/lots/{lot}").data["available"], "20.000"
        )

    def test_cross_lot_qr_and_private_file(self):
        from compost.models import Process, Evidence
        from traceability.models import Lot
        from django.core.files.uploadedfile import SimpleUploadedFile
        import tempfile
        from django.test import override_settings

        other = Institution.objects.create(name="Institución ajena")
        lot = Lot.objects.create(institution=other, provenance="simulado")
        process = Process.objects.create(
            institution=other, provenance="simulado", actor=self.operator
        )
        with tempfile.TemporaryDirectory() as directory, override_settings(
            MEDIA_ROOT=directory
        ):
            e = Evidence.objects.create(
                institution=other,
                process=process,
                receiver="Demo",
                date="2026-11-15",
                description="Privado",
                actor=self.operator,
                file=SimpleUploadedFile("document.pdf", b"%PDF-1.4 demo"),
            )
            for path in [
                f"lots/{lot.id}",
                f"lots/qr/{lot.public_id}",
                f"lots/{lot.id}/image",
                f"evidence/{e.id}/download",
                f"compost/processes/{process.id}",
            ]:
                self.assertEqual(self.client.get("/api/" + path).status_code, 404)
        self.assertEqual(self.client.get("/api/lots").data, [])
        self.assertEqual(self.client.get("/api/compost/processes").data, [])

    def test_administrator_roles_and_catalog(self):
        admin = User.objects.create_user("admin", password="Test-only-pass-123!")
        Membership.objects.create(
            user=admin, institution=self.institution, role="administrador"
        )
        self.client.force_authenticate(admin)
        response = self.post(
            "users",
            {
                "username": "new_operator",
                "password": "New-Test-only-pass-123!",
                "role": "operador",
            },
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(
            self.client.patch(
                f"/api/users/{admin.pk}", {"role": "gestor"}, format="json"
            ).status_code,
            400,
        )
        self.assertEqual(self.post("generations", {}).status_code, 403)
        self.assertEqual(
            self.post(
                "materials", {"name": "Peligroso", "category": "especial"}
            ).status_code,
            201,
        )
        self.client.force_authenticate(self.operator)
        material = Material.objects.get(name="Peligroso")
        self.assertEqual(
            self.post(
                "generations",
                {
                    "area": self.area.id,
                    "material": material.id,
                    "kg": "1",
                    "unit": "kg",
                    "date": "2026-11-15T12:00:00-05:00",
                    "provenance": "simulado",
                },
            ).status_code,
            400,
        )
