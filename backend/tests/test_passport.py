from django.test import TestCase
from tests.fixtures import Fixture
from traceability.models import Lot
from organizations.models import Institution


class PassportTests(Fixture, TestCase):
    def passport(self, lot_id):
        uuid = Lot.objects.get(pk=lot_id).public_id
        return self.client.get(f"/api/v2/lots/{uuid}/passport")

    def test_balance_timeline_and_qr_contract(self):
        lot, g = self.lot()
        self.post(
            f"lots/{lot}/movements",
            {"type": "logistico", "kg": "20", "unit": "kg", "destination": "Campus"},
        )
        self.post(
            f"lots/{lot}/movements",
            {
                "type": "entrega",
                "kg": "5",
                "unit": "kg",
                "destination": "Gestor externo",
            },
        )
        r = self.passport(lot)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.data["balance"],
            {"assigned": "25.000", "available": "20.000", "consumed": "5.000"},
        )
        self.assertEqual(
            next(e for e in r.data["events"] if e["kind"] == "logistico")[
                "balance_effect"
            ],
            "0.000",
        )
        self.assertEqual(
            next(e for e in r.data["events"] if e["kind"] == "entrega")[
                "balance_effect"
            ],
            "-5.000",
        )
        self.assertIsNone(
            next(e for e in r.data["events"] if e["kind"] == "lote")["actor"]
        )
        self.assertEqual(r.data["sources"][0]["generation"], g)
        self.assertEqual(r.data["processes"], [])
        self.assertEqual(
            self.client.get(f'/api/lots/qr/{r.data["lot"]["public_id"]}').status_code,
            200,
        )

    def test_private_and_missing(self):
        lot, _ = self.lot()
        self.client.force_authenticate(self.reader)
        self.assertEqual(self.passport(lot).status_code, 200)
        other = Lot.objects.create(
            institution=Institution.objects.create(name="Ajena"), provenance="simulado"
        )
        self.assertEqual(self.passport(other.pk).status_code, 404)
        self.client.force_authenticate(None)
        self.assertEqual(self.passport(lot).status_code, 401)

    def test_shared_process_output_is_not_attributed_to_lot(self):
        first, _ = self.lot()
        second, _ = self.lot()
        p = self.post("compost/processes", {"provenance": "simulado"}).data["id"]
        for lot in [first, second]:
            self.post(
                f"compost/processes/{p}/inputs", {"lot": lot, "kg": "10", "unit": "kg"}
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
        d = self.passport(first).data
        self.assertEqual(d["balance"]["consumed"], "10.000")
        process = d["processes"][0]
        self.assertEqual(process["lot_input"], "10.000")
        self.assertEqual(process["total_input"], "20.000")
        self.assertEqual(process["output"], "8.000")
        self.assertTrue(process["shared"])
        self.assertEqual(
            next(e for e in d["events"] if e["kind"] == "salida")["balance_effect"],
            "0.000",
        )
