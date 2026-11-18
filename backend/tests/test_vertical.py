from django.test import TestCase
from tests.fixtures import Fixture


class VerticalTests(Fixture, TestCase):
    def test_vertical(self):
        lot, generation = self.lot()
        process = self.post("compost/processes", {"provenance": "simulado"}).data["id"]
        key = "entrada-test"
        data = {"lot": lot, "kg": "20.000", "unit": "kg"}
        first = self.post(f"compost/processes/{process}/inputs", data, key)
        self.assertEqual(first.status_code, 201, first.data)
        self.assertEqual(
            self.post(f"compost/processes/{process}/inputs", data, key).data, first.data
        )
        self.assertEqual(
            self.post(
                f"lots/{lot}/movements",
                {"kg": "6", "unit": "kg", "type": "entrega", "destination": "Gestor"},
            ).status_code,
            409,
        )
        self.assertEqual(self.client.get(f"/api/lots/{lot}").data["available"], "5.000")
        self.assertEqual(
            self.post(
                f"generations/{generation}/correct", {"kg": "24", "reason": "Error"}
            ).status_code,
            403,
        )
        self.assertEqual(
            self.post(
                f"compost/processes/{process}/finalize",
                {
                    "kg": "8",
                    "unit": "kg",
                    "destination": "Huerta",
                    "provenance": "simulado",
                },
            ).status_code,
            201,
        )
        self.client.force_authenticate(self.manager)
        self.assertEqual(
            self.post(
                f"compost/processes/{process}/verify",
                {"decision": "confirmado", "reason": "Revisión"},
            ).status_code,
            400,
        )
        evidence = {
            "receiver": "Huerta demo",
            "reference": "ACTA-SIMULADA-001",
            "description": "Comprobante simulado de entrega",
            "date": "2026-11-15",
        }
        self.assertEqual(
            self.post(f"compost/processes/{process}/evidence", evidence).status_code,
            201,
        )
        self.assertEqual(
            self.post(
                f"compost/processes/{process}/verify",
                {"decision": "confirmado", "reason": "Verificación de ejemplo"},
            ).status_code,
            201,
        )
        dashboard = self.client.get("/api/dashboard").data
        self.assertEqual(dashboard["generated"], "25.000")
        self.assertEqual(dashboard["verified_compost"], "20.000")
        self.assertEqual(dashboard["pending"], "5.000")
        self.assertEqual(dashboard["rate"], "80.00")
        self.assertEqual(
            self.client.get("/api/dashboard?provenance=medido").data["rate"], None
        )
        self.assertEqual(
            self.post(
                f"generations/{generation}/correct", {"kg": "24", "reason": "Error"}
            ).status_code,
            409,
        )

    def test_invalid_mass_and_reader(self):
        for kg in ["0", "-1", "abc", "1.0001", "NaN", "Infinity"]:
            response = self.post(
                "generations",
                {
                    "area": self.area.id,
                    "material": self.material.id,
                    "kg": kg,
                    "unit": "kg",
                    "provenance": "simulado",
                    "date": "2026-11-15T10:00:00-05:00",
                },
            )
            self.assertEqual(response.status_code, 400, response.data)
        self.client.force_authenticate(self.reader)
        self.assertEqual(self.post("generations", {}).status_code, 403)
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get("/api/generations").status_code, 401)
