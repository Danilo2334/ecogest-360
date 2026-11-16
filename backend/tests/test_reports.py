from django.utils import timezone
from django.db import connection
from tests.fixtures import Fixture
from django.test import TestCase
from reports.csv_export import safe


class ReportTests(Fixture, TestCase):
    def test_external_delivery_not_accredited(self):
        lot, _ = self.lot()
        self.post(
            f"lots/{lot}/movements",
            {
                "kg": "5",
                "unit": "kg",
                "type": "entrega",
                "destination": "Gestor externo",
            },
        )
        d = self.client.get("/api/dashboard").data
        self.assertEqual(d["delivered"], "5.000")
        self.assertEqual(d["verified_compost"], "0.000")
        self.assertEqual(d["pending"], "25.000")
        self.assertEqual(d["available"], "20.000")

    def test_csv_escaping_and_persistence(self):
        self.material.name = '=SUM(1,2) "simulado"'
        self.material.save()
        g = self.generation()
        content = self.client.get(
            "/api/reports/generation.csv?provenance=simulado"
        ).content.decode("utf-8-sig")
        import csv, io

        row = list(csv.DictReader(io.StringIO(content)))[0]
        self.assertTrue(row["material"].startswith("'="))
        self.assertEqual(row["generated"], "25.000")
        self.assertEqual(row["provenance"], "simulado")
        self.assertEqual(self.client.get(f"/api/generations/{g}").data["kg"], "25.000")

    def test_bad_filters(self):
        for query in [
            "area=no",
            "provenance=real",
            "generated_from=invalid",
            "cutoff=no",
            "generated_from=2026-11-16&generated_to=2026-11-15",
        ]:
            self.assertEqual(
                self.client.get("/api/dashboard?" + query).status_code, 400
            )
