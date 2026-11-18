from django.test import TestCase
from tests.fixtures import Fixture
from waste.models import Generation
from traceability.models import Movement
from catalog.models import Material


class ScenarioTests(Fixture, TestCase):
    def test_verified_compost_example_25_20_8(self):
        lot, _ = self.lot()
        p = self.post("compost/processes", {"provenance": "simulado"}).data["id"]
        self.post(
            f"compost/processes/{p}/inputs", {"lot": lot, "kg": "20", "unit": "kg"}
        )
        self.post(
            f"compost/processes/{p}/finalize",
            {
                "kg": "8",
                "unit": "kg",
                "provenance": "simulado",
                "destination": "Jardín simulado",
            },
        )
        self.post(
            f"compost/processes/{p}/evidence",
            {
                "receiver": "Demo",
                "date": "2026-11-15",
                "reference": "simulado:test",
                "description": "Prueba simulada",
            },
        )
        self.client.force_authenticate(self.manager)
        self.post(
            f"compost/processes/{p}/verify",
            {"decision": "confirmado", "reason": "Prueba simulada"},
        )
        response = self.preview("3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["result"],
            {
                "generated": "25.000",
                "verified_compost": "23.000",
                "pending": "2.000",
                "rate": "92.00",
            },
        )
        self.assertEqual(response.data["delta"]["rate_points"], "12.00")

    def preview(self, amount="0", hypothesis="increase_compost", **kwargs):
        return self.client.post(
            "/api/v2/scenarios/preview",
            dict(
                filters={
                    "provenance": "simulado",
                    "generated_from": "2026-11-15",
                    "generated_to": "2026-11-15",
                },
                amount=amount,
                hypothesis=hypothesis,
                **kwargs,
            ),
            format="json",
        )

    def test_eligible_never_counts_allocations_twice_and_no_write(self):
        lot, _ = self.lot()
        self.post(
            f"lots/{lot}/movements",
            {"type": "entrega", "kg": "20", "unit": "kg", "destination": "Externo"},
        )
        counts = (Generation.objects.count(), Movement.objects.count())
        r = self.preview("5")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["eligible"], "5.000")
        self.assertEqual(r.data["result"]["rate"], "20.00")
        self.assertEqual(self.preview("6").status_code, 400)
        self.assertEqual(counts, (Generation.objects.count(), Movement.objects.count()))

    def test_zero_denominator_and_invalid_amounts(self):
        g = self.generation("10")
        material = Material.objects.create(
            institution=self.institution, name="No aprovechable", category="negro"
        )
        Generation.objects.filter(pk=g).update(material=material)
        r = self.preview("10", "reduce_nonrecoverable")
        self.assertEqual(r.status_code, 200)
        self.assertIsNone(r.data["result"]["rate"])
        for value in ["-1", "NaN", "Infinity", "0.0001", True]:
            self.assertEqual(self.preview(value).status_code, 400)

    def test_stale_base_and_estimated(self):
        g = self.generation()
        first = self.preview()
        self.assertEqual(first.status_code, 200)
        Generation.objects.filter(pk=g).update(kg="30")
        self.assertEqual(
            self.preview("1", base_token=first.data["base_token"]).status_code, 409
        )
        Generation.objects.filter(pk=g).update(provenance="estimado")
        r = self.client.post(
            "/api/v2/scenarios/preview",
            {
                "filters": {
                    "provenance": "estimado",
                    "generated_from": "2026-11-15",
                    "generated_to": "2026-11-15",
                },
                "amount": "1",
                "hypothesis": "increase_compost",
            },
            format="json",
        )
        self.assertEqual(r.status_code, 400)

    def test_scope_filters_and_no_auth(self):
        self.generation()
        self.client.force_authenticate(self.reader)
        self.assertEqual(self.preview().status_code, 200)
        r = self.client.post(
            "/api/v2/scenarios/preview",
            {
                "filters": {
                    "provenance": "simulado",
                    "generated_from": "2026-11-15",
                    "generated_to": "2026-11-15",
                    "area": "99999",
                },
                "amount": "1",
                "hypothesis": "increase_compost",
            },
            format="json",
        )
        self.assertEqual(r.status_code, 400)
        self.client.force_authenticate(None)
        self.assertEqual(self.preview().status_code, 401)
