from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from tests.fixtures import Fixture
from waste.models import Generation
from organizations.models import Institution, Area


class ObservatoryTests(Fixture, TestCase):
    def params(self):
        end = timezone.localdate() - timedelta(days=1)
        return {
            "generated_from": str(end),
            "generated_to": str(end),
            "provenance": "simulado",
        }

    def seed(self, weight, date):
        return Generation.objects.create(
            institution=self.institution,
            area=self.area,
            material=self.material,
            actor=self.operator,
            kg=weight,
            provenance="simulado",
            date=str(date) + "T12:00:00-05:00",
        )

    def test_comparison_and_series(self):
        p = self.params()
        end = timezone.localdate() - timedelta(days=1)
        self.seed("25", end)
        self.seed("20", end - timedelta(days=1))
        response = self.client.get("/api/observatory", p)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data["summary"]["generated"], "25.000")
        self.assertEqual(data["comparison"]["percent"], "25.00")
        self.assertEqual(data["comparison"]["absolute"], "5.000")
        self.assertEqual(len(data["series"]), 1)
        self.assertEqual(data["areas"][0]["generated"], "25.000")
        self.assertEqual(data["summary"]["cutoff"], data["context"]["cutoff"])
        for finding in data["insights"]:
            self.assertTrue(finding["interpretation"])
            self.assertTrue(finding["suggestion"])
        top = next(x for x in data["insights"] if x["code"] == "largest_area")
        self.assertEqual(top["area"], self.area.pk)

    def test_missing_base_and_mixed_provenance(self):
        self.seed("25", self.params()["generated_to"])
        data = self.client.get("/api/observatory", self.params()).data
        self.assertFalse(data["comparison"]["available"])
        self.assertIsNone(data["comparison"]["percent"])
        mixed = self.client.get("/api/observatory").data
        self.assertIsNone(mixed["summary"]["rate"])
        self.assertFalse(mixed["comparison"]["available"])
        self.assertEqual(mixed["provenance_totals"][0]["generated"], "25.000")

    def test_period_validation_and_current_day(self):
        p = self.params()
        p["generated_to"] = str(timezone.localdate())
        data = self.client.get("/api/observatory", p).data
        self.assertFalse(data["comparison"]["available"])
        self.assertEqual(
            self.client.get(
                "/api/observatory", {"generated_from": "invalid"}
            ).status_code,
            400,
        )
        self.assertFalse(
            self.client.get("/api/observatory", {"provenance": "simulado"}).data[
                "comparison"
            ]["available"]
        )

    def test_reader_scope_and_no_mutation(self):
        self.seed("25", self.params()["generated_to"])
        self.client.force_authenticate(self.reader)
        self.assertEqual(
            self.client.get("/api/observatory", self.params()).status_code, 200
        )
        self.assertEqual(
            self.client.get("/api/observatory", {**self.params(), "area": 999999}).data[
                "summary"
            ]["generated"],
            "0.000",
        )
        before = Generation.objects.count()
        self.assertNotEqual(self.post("observatory", {}).status_code, 201)
        self.assertEqual(Generation.objects.count(), before)
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get("/api/observatory").status_code, 401)

    def test_duplicate_area_names_and_sparse_days(self):
        end = timezone.localdate() - timedelta(days=1)
        self.seed("10", end)
        other = Area.objects.create(
            institution=self.institution, site=self.area.site, name=self.area.name
        )
        g = self.seed("5", end - timedelta(days=2))
        g.area = other
        g.save()
        data = self.client.get(
            "/api/observatory",
            {**self.params(), "generated_from": str(end - timedelta(days=2))},
        ).data
        self.assertEqual(len(data["areas"]), 2)
        self.assertEqual(len(data["series"]), 2)
        self.assertEqual(data["summary"]["generated"], "15.000")

    def test_cutoff_before_period_prevents_comparison(self):
        p = self.params()
        p["cutoff"] = "2020-01-01T00:00:00Z"
        self.assertFalse(
            self.client.get("/api/observatory", p).data["comparison"]["available"]
        )

    def test_v1_accredited_formula_is_reused(self):
        lot, generation = self.lot()
        process = self.post("compost/processes", {"provenance": "simulado"}).data["id"]
        self.post(
            f"compost/processes/{process}/inputs",
            {"lot": lot, "kg": "20", "unit": "kg"},
        )
        self.post(
            f"compost/processes/{process}/finalize",
            {
                "kg": "8",
                "unit": "kg",
                "provenance": "simulado",
                "destination": "Huerta simulada",
            },
        )
        self.post(
            f"compost/processes/{process}/evidence",
            {
                "reference": "SIMULADO",
                "receiver": "Demo",
                "date": "2026-11-15",
                "description": "Comprobante de prueba simulado",
            },
        )
        self.client.force_authenticate(self.manager)
        self.post(
            f"compost/processes/{process}/verify",
            {"decision": "confirmado", "reason": "Verificación simulada"},
        )
        a = self.client.get("/api/observatory", {"provenance": "simulado"}).data[
            "summary"
        ]
        b = self.client.get("/api/dashboard", {"provenance": "simulado"}).data
        for key in ["generated", "verified_compost", "pending", "available", "rate"]:
            self.assertEqual(a[key], b[key])
        self.assertEqual(a["verified_compost"], "20.000")
        self.assertEqual(a["rate"], "80.00")

    def test_bogota_date_and_other_institution(self):
        g = self.seed("25", "2026-11-14")
        g.date = "2026-11-15T02:00:00Z"
        g.save()
        data = self.client.get(
            "/api/observatory",
            {
                "generated_from": "2026-11-14",
                "generated_to": "2026-11-14",
                "provenance": "simulado",
            },
        ).data
        self.assertEqual(data["series"][0]["date"], "2026-11-14")
        other = Institution.objects.create(name="Ajena")
        g.institution = other
        g.save()
        data = self.client.get("/api/observatory", {"provenance": "simulado"}).data
        self.assertEqual(data["summary"]["generated"], "0.000")
        self.assertEqual(data["areas"], [])


from django.test import TransactionTestCase
from concurrent.futures import ThreadPoolExecutor
from django.db import connection, close_old_connections
from time import perf_counter
from rest_framework.test import APIClient


class ObservatoryPerformanceTests(Fixture, TransactionTestCase):
    def test_ten_thousand_records_hundred_samples(self):
        end = timezone.localdate() - timedelta(days=1)
        Generation.objects.bulk_create(
            [
                Generation(
                    institution=self.institution,
                    area=self.area,
                    material=self.material,
                    actor=self.operator,
                    kg="1",
                    provenance="simulado",
                    date=str(end) + "T12:00:00-05:00",
                )
                for _ in range(10000)
            ],
            batch_size=1000,
        )

        def worker(_):
            close_old_connections()
            try:
                client = APIClient()
                client.force_authenticate(self.operator)
                start = perf_counter()
                response = client.get(
                    "/api/observatory",
                    {
                        "provenance": "simulado",
                        "generated_from": str(end),
                        "generated_to": str(end),
                    },
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["summary"]["generated"], "10000.000")
                return perf_counter() - start
            finally:
                connection.close()

        with ThreadPoolExecutor(max_workers=10) as pool:
            samples = sorted(pool.map(worker, range(100)))
        print(
            f"OBSERVATORY: 10000 rows / 10 readers / 100 requests: p95={samples[94]:.3f}s"
        )
        self.assertLessEqual(samples[94], 2)
