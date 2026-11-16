import csv
import io
from django.test import TestCase
from compost.models import Output, Process, Verification
from tests.fixtures import Fixture


class CompostProvenanceTests(Fixture, TestCase):
    """Synthetic isolated fixtures; 'medido' exercises a label, not field measurements."""

    def prepare(self, origin, finalize=True):
        self.client.force_authenticate(self.operator)
        g = self.post(
            "generations",
            {
                "area": self.area.id,
                "material": self.material.id,
                "kg": "25",
                "unit": "kg",
                "provenance": origin,
                "date": "2026-11-15T10:00:00-05:00",
                "method": "Fixture de prueba, no medicion de campo",
            },
        )
        self.assertEqual(g.status_code, 201, g.data)
        lot = self.post(
            "lots", {"sources": [{"generation": g.data["id"], "kg": "25"}]}
        ).data["id"]
        p = self.post("compost/processes", {"provenance": origin}).data["id"]
        result = self.post(
            f"compost/processes/{p}/inputs", {"lot": lot, "kg": "20", "unit": "kg"}
        )
        self.assertEqual(result.status_code, 201)
        if finalize:
            result = self.post(
                f"compost/processes/{p}/finalize",
                {
                    "kg": "8",
                    "unit": "kg",
                    "provenance": origin,
                    "destination": "Destino de fixture",
                },
            )
            self.assertEqual(result.status_code, 201)
            result = self.post(
                f"compost/processes/{p}/evidence",
                {
                    "reference": "FIXTURE-NO-CAMPO",
                    "receiver": "Huerta de fixture",
                    "description": "Comprobante sintetico para prueba aislada",
                    "date": "2026-11-15",
                },
            )
            self.assertEqual(result.status_code, 201)
        return p, lot

    def confirm(self, p, key=None):
        self.client.force_authenticate(self.manager)
        return self.post(
            f"compost/processes/{p}/verify",
            {"decision": "confirmado", "reason": "Revision de fixture independiente"},
            key,
        )

    def assert_report(self, origin, accredited):
        panel = self.client.get("/api/dashboard", {"provenance": origin}).data
        self.assertEqual(panel["generated"], "25.000")
        self.assertEqual(panel["verified_compost"], accredited)
        content = self.client.get(
            "/api/reports/generation.csv", {"provenance": origin}
        ).content
        rows = list(csv.DictReader(io.StringIO(content.decode("utf-8-sig"))))
        self.assertEqual(rows[0]["verified_compost"], accredited)
        self.assertEqual(rows[0]["provenance"], origin)
        return panel

    def test_estimated_cannot_be_confirmed(self):
        p, lot = self.prepare("estimado")
        for _ in range(2):
            result = self.confirm(p, "estimated-retry")
            self.assertEqual(result.status_code, 400, result.data)
        self.assertFalse(Verification.objects.filter(process_id=p).exists())
        self.assertEqual(Process.objects.get(pk=p).provenance, "estimado")
        self.assertEqual(Output.objects.get(process_id=p).provenance, "estimado")
        self.assertEqual(self.client.get(f"/api/lots/{lot}").data["available"], "5.000")
        panel = self.assert_report("estimado", "0.000")
        self.assertEqual(panel["pending"], "25.000")

    def test_measured_independent_output_and_idempotent_confirmation(self):
        p, _ = self.prepare("medido")
        first = self.confirm(p, "measured-confirmation")
        self.assertEqual(first.status_code, 201, first.data)
        self.assertEqual(self.confirm(p, "measured-confirmation").data, first.data)
        self.assertEqual(Verification.objects.filter(process_id=p).count(), 1)
        panel = self.assert_report("medido", "20.000")
        self.assertEqual(panel["rate"], "80.00")
        self.assertEqual(panel["pending"], "5.000")
        self.assertEqual(str(Output.objects.get(process_id=p).kg), "8.000")

    def test_simulated_stays_separate_from_measured(self):
        p, _ = self.prepare("simulado")
        self.assertEqual(self.confirm(p).status_code, 201)
        self.assert_report("simulado", "20.000")
        self.assertEqual(
            self.client.get("/api/dashboard", {"provenance": "medido"}).data[
                "generated"
            ],
            "0.000",
        )
        self.assertEqual(Process.objects.get(pk=p).provenance, "simulado")
        self.assertEqual(Output.objects.get(process_id=p).provenance, "simulado")

    def test_measured_cannot_finalize_as_estimated(self):
        p, _ = self.prepare("medido", finalize=False)
        result = self.post(
            f"compost/processes/{p}/finalize",
            {
                "kg": "8",
                "unit": "kg",
                "provenance": "estimado",
                "destination": "Fixture",
            },
        )
        self.assertEqual(result.status_code, 400)
        self.assertFalse(Output.objects.filter(process_id=p).exists())
        self.assertEqual(Process.objects.get(pk=p).state, "en_proceso")

    def test_incompatible_historical_output_cannot_be_confirmed(self):
        p, _ = self.prepare("medido")
        Output.objects.filter(process_id=p).update(provenance="estimado")
        self.assertEqual(self.confirm(p).status_code, 400)
        self.assertFalse(Verification.objects.filter(process_id=p).exists())

    def test_historical_estimated_confirmation_excluded_without_erasing(self):
        p, _ = self.prepare("estimado")
        Verification.objects.create(
            institution=self.institution,
            process_id=p,
            actor=self.manager,
            decision="confirmado",
            reason="Fixture historico anterior a regla",
        )
        self.assert_report("estimado", "0.000")
        self.assertEqual(Verification.objects.filter(process_id=p).count(), 1)
