from django.utils import timezone
from datetime import timedelta
from tests.fixtures import Fixture
from django.test import TestCase
from waste.models import Generation
from core.models import Incident
from compost.models import Verification


class CompostRulesTests(Fixture, TestCase):
    def process(self):
        lot, g = self.lot()
        p = self.post("compost/processes", {"provenance": "simulado"}).data["id"]
        self.post(
            f"compost/processes/{p}/inputs", {"lot": lot, "kg": "25", "unit": "kg"}
        )
        return p, lot, g

    def test_evidence_permissions_and_immutable_confirmation(self):
        p, lot, g = self.process()
        self.assertEqual(
            self.post(
                f"compost/processes/{p}/verify",
                {"decision": "confirmado", "reason": "Intento"},
            ).status_code,
            403,
        )
        self.post(
            f"compost/processes/{p}/finalize",
            {
                "kg": "8",
                "unit": "kg",
                "destination": "Huerta",
                "provenance": "simulado",
            },
        )
        from django.core.files.uploadedfile import SimpleUploadedFile

        upload = SimpleUploadedFile(
            "script.pdf", b"<script>no</script>", content_type="application/pdf"
        )
        response = self.client.post(
            f"/api/compost/processes/{p}/evidence",
            {
                "file": upload,
                "receiver": "Demo",
                "description": "Demo",
                "date": "2026-11-15",
            },
            format="multipart",
            HTTP_IDEMPOTENCY_KEY="file-invalid",
        )
        self.assertEqual(response.status_code, 400)
        e = self.post(
            f"compost/processes/{p}/evidence",
            {
                "reference": "ACTA-SIMULADA",
                "receiver": "Huerta",
                "description": "Demo verificable",
                "date": "2026-11-15",
            },
        )
        self.assertEqual(e.status_code, 201)
        self.client.force_authenticate(self.manager)
        before = timezone.now() - timedelta(seconds=1)
        self.post(
            f"compost/processes/{p}/verify",
            {"decision": "confirmado", "reason": "Revisé destino y pesaje"},
        )
        self.assertEqual(
            self.client.get("/api/dashboard", {"cutoff": before.isoformat()}).data[
                "verified_compost"
            ],
            "0.000",
        )
        self.assertEqual(
            self.client.get("/api/dashboard").data["verified_compost"], "25.000"
        )
        self.assertEqual(
            self.post(
                f"compost/processes/{p}/verify",
                {"decision": "confirmado", "reason": "Otro"},
            ).status_code,
            409,
        )
        self.assertEqual(
            Verification.objects.filter(process_id=p, decision="confirmado").count(), 1
        )
        self.assertEqual(
            self.post(
                f"compost/processes/{p}/evidence", {"reference": "OTRA"}
            ).status_code,
            409,
        )
        self.client.force_authenticate(self.operator)
        self.assertEqual(self.post(f"lots/{lot}/close", {}).status_code, 201)
        self.assertEqual(
            self.post(
                f"lots/{lot}/movements",
                {"kg": "1", "unit": "kg", "type": "logistico", "destination": "Otro"},
            ).status_code,
            409,
        )
        self.assertEqual(
            self.post(
                "incidents", {"entity": f"lot:{lot}", "reason": "Error histórico"}
            ).status_code,
            201,
        )
        self.assertEqual(Incident.objects.count(), 1)

    def test_cohort_sources_and_nonorganic(self):
        p, lot, g = self.process()
        g2 = self.generation("10")
        Generation.objects.filter(pk=g2).update(
            date=timezone.now() - timedelta(days=60)
        )
        lot2 = self.post("lots", {"sources": [{"generation": g2, "kg": "10"}]}).data[
            "id"
        ]
        self.post(
            f"compost/processes/{p}/inputs", {"lot": lot2, "kg": "10", "unit": "kg"}
        )
        self.post(
            f"compost/processes/{p}/finalize",
            {
                "kg": "9",
                "unit": "kg",
                "provenance": "simulado",
                "destination": "Huerta",
            },
        )
        self.post(
            f"compost/processes/{p}/evidence",
            {
                "reference": "ACTA",
                "receiver": "Huerta",
                "description": "Demo",
                "date": "2026-11-15",
            },
        )
        self.client.force_authenticate(self.manager)
        self.post(
            f"compost/processes/{p}/verify",
            {"decision": "confirmado", "reason": "Completo"},
        )
        result = self.client.get(
            "/api/dashboard",
            {"generated_from": "2026-11-15", "generated_to": "2026-11-15"},
        ).data
        self.assertEqual(result["generated"], "25.000")
        self.assertEqual(result["verified_compost"], "25.000")
        self.client.force_authenticate(self.operator)
        self.material.category = "negro"
        self.material.save()
        lot3, _ = self.lot()
        p2 = self.post("compost/processes", {"provenance": "simulado"}).data["id"]
        self.assertEqual(
            self.post(
                f"compost/processes/{p2}/inputs", {"lot": lot3, "kg": "1", "unit": "kg"}
            ).status_code,
            400,
        )

    def test_private_upload_and_control(self):
        import tempfile
        from django.test import override_settings
        from django.core.files.uploadedfile import SimpleUploadedFile

        p, lot, g = self.process()
        control = self.post(
            f"compost/processes/{p}/measurements",
            {
                "type": "temperatura",
                "value": "35.2",
                "unit": "C",
                "date": "2026-11-15T12:00:00-05:00",
            },
        )
        self.assertEqual(control.status_code, 201)
        with tempfile.TemporaryDirectory() as folder, override_settings(
            MEDIA_ROOT=folder
        ):
            document = SimpleUploadedFile(
                "destino.pdf",
                b"%PDF-1.4\nDocumento SIMULADO\n%%EOF",
                content_type="application/pdf",
            )
            result = self.client.post(
                f"/api/compost/processes/{p}/evidence",
                {
                    "file": document,
                    "receiver": "Huerta",
                    "date": "2026-11-15",
                    "description": "Documento simulado",
                },
                format="multipart",
                HTTP_IDEMPOTENCY_KEY="private-upload",
            )
            self.assertEqual(result.status_code, 201, result.data)
            response = self.client.get(f"/api/evidence/{result.data['id']}/download")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"SIMULADO", b"".join(response.streaming_content))
            self.client.force_authenticate(None)
            self.assertEqual(
                self.client.get(
                    f"/api/evidence/{result.data['id']}/download"
                ).status_code,
                401,
            )
            response.close()
