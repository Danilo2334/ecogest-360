from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from tests.fixtures import Fixture
from compost.models import Evidence
from traceability.models import Lot


class AuditRegressionTests(Fixture, TestCase):
    def test_null_required_evidence_is_rejected(self):
        p = self.post("compost/processes", {"provenance": "simulado"}).data["id"]
        valid = {
            "reference": "SIMULADO-AUDITORIA",
            "receiver": "Huerta demo",
            "description": "Comprobante simulado",
            "date": "2026-11-15",
        }
        for field in ["reference", "receiver", "description"]:
            with self.subTest(field=field):
                result = self.post(
                    f"compost/processes/{p}/evidence", {**valid, field: None}
                )
                self.assertEqual(result.status_code, 400)
        self.assertEqual(Evidence.objects.count(), 0)

    def test_unexpected_upload_field_is_rejected(self):
        p = self.post("compost/processes", {"provenance": "simulado"}).data["id"]
        result = self.client.post(
            f"/api/compost/processes/{p}/evidence",
            {"unexpected": SimpleUploadedFile("demo.pdf", b"%PDF-1.4 simulated")},
            format="multipart",
            HTTP_IDEMPOTENCY_KEY="audit-upload",
        )
        self.assertEqual(result.status_code, 400)
        self.assertEqual(Evidence.objects.count(), 0)

    def test_consultant_cannot_write_any_action(self):
        self.client.force_authenticate(self.reader)
        paths = [
            "sites",
            "areas",
            "materials",
            "users",
            "generations",
            "generations/1/correct",
            "generations/1/review",
            "lots",
            "lots/1/movements",
            "lots/1/close",
            "compost/processes",
            "compost/processes/1/inputs",
            "compost/processes/1/measurements",
            "compost/processes/1/finalize",
            "compost/processes/1/evidence",
            "compost/processes/1/verify",
            "incidents",
        ]
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(self.post(path, {}).status_code, 403)
        for path in ["institution", "sites/1", "areas/1", "materials/1", "users/1"]:
            self.assertEqual(
                self.client.patch("/api/" + path, {}, format="json").status_code, 403
            )

    def test_qr_image_and_authorized_lookup(self):
        lot_id, _ = self.lot()
        lot = Lot.objects.get(pk=lot_id)
        response = self.client.get(f"/api/lots/{lot_id}/image")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b"".join(response.streaming_content).startswith(b"\x89PNG\r\n\x1a\n")
        )
        result = self.client.get(f"/api/lots/qr/{lot.public_id}")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data["id"], lot_id)
        self.assertEqual(
            APIClient().get(f"/api/lots/qr/{lot.public_id}").status_code, 401
        )
