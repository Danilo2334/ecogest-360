from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from django.db import close_old_connections, connection
from django.test import TransactionTestCase
from tests.fixtures import Fixture
from django.test import TestCase
from core.idempotency import execute
from core.errors import Conflict
from organizations.models import Membership
from traceability.models import Lot, Movement
from traceability.services import move


class ConcurrencyTests(TransactionTestCase):
    setUp = Fixture.setUp
    post = Fixture.post
    generation = Fixture.generation
    lot = Fixture.lot

    def run_race(self, keys):
        lot, _ = self.lot()
        self.post(
            f"lots/{lot}/movements",
            {"kg": "20", "unit": "kg", "type": "entrega", "destination": "Primera"},
        )
        barrier = Barrier(2)

        def worker(key):
            close_old_connections()
            try:
                m = Membership.objects.get(user_id=self.operator.id)
                barrier.wait(timeout=10)
                payload = {
                    "kg": "4",
                    "unit": "kg",
                    "type": "entrega",
                    "destination": "Prueba",
                }
                try:
                    return execute(
                        m,
                        f"lots/{lot}/movements",
                        key,
                        payload,
                        lambda: move(m, lot, payload),
                    )["available"]
                except Conflict:
                    return "conflict"
            finally:
                connection.close()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(worker, keys))
        self.assertEqual(Lot.objects.get(pk=lot).available(), 1)
        self.assertEqual(Movement.objects.filter(lot_id=lot).count(), 2)
        return results

    def test_distinct_consumptions(self):
        self.assertCountEqual(self.run_race(["one", "two"]), ["1.000", "conflict"])

    def test_same_operation(self):
        self.assertEqual(self.run_race(["same", "same"]), ["1.000", "1.000"])

    def concurrent(self, actions):
        barrier = Barrier(len(actions))

        def worker(action):
            close_old_connections()
            try:
                from django.db import transaction

                barrier.wait(timeout=10)
                try:
                    with transaction.atomic():
                        return action()
                except Conflict:
                    return "conflict"
            finally:
                connection.close()

        with ThreadPoolExecutor(max_workers=len(actions)) as pool:
            return list(pool.map(worker, actions))

    def test_correction_competes_with_allocation(self):
        from waste.services import correct
        from traceability.services import create
        from waste.models import Generation

        g = self.generation()
        operator = Membership.objects.get(user=self.operator)
        manager = Membership.objects.get(user=self.manager)
        results = self.concurrent(
            [
                lambda: create(operator, {"sources": [{"generation": g, "kg": "25"}]}),
                lambda: correct(
                    manager, g, {"kg": "24", "unit": "kg", "reason": "Corrección"}
                ),
            ]
        )
        self.assertEqual(sum(r == "conflict" for r in results), 1)
        generation = Generation.objects.get(pk=g)
        self.assertIn(generation.kg, [24, 25])
        self.assertEqual(
            generation.allocations.count(), 1 if generation.kg == 25 else 0
        )

    def test_input_competes_with_finalization_and_double_verification(self):
        from compost import services
        from compost.models import Process, Input, Verification
        from django.db.models import Sum

        lot, _ = self.lot()
        p = self.post("compost/processes", {"provenance": "simulado"}).data["id"]
        self.post(
            f"compost/processes/{p}/inputs", {"lot": lot, "kg": "20", "unit": "kg"}
        )
        operator = Membership.objects.get(user=self.operator)
        results = self.concurrent(
            [
                lambda: services.add_input(
                    operator, p, {"lot": lot, "kg": "4", "unit": "kg"}
                ),
                lambda: services.finalize(
                    operator,
                    p,
                    {
                        "kg": "8",
                        "unit": "kg",
                        "destination": "Demo",
                        "provenance": "simulado",
                    },
                ),
            ]
        )
        self.assertEqual(Process.objects.get(pk=p).state, "finalizado")
        total = Input.objects.filter(process_id=p).aggregate(v=Sum("movement__kg"))["v"]
        self.assertIn(total, [20, 24])
        self.assertEqual(Lot.objects.get(pk=lot).available(), 25 - total)
        self.post(
            f"compost/processes/{p}/evidence",
            {
                "receiver": "Demo",
                "date": "2026-11-15",
                "reference": "ACTA-DEMO",
                "description": "Simulado",
            },
        )
        manager = Membership.objects.get(user=self.manager)
        results = self.concurrent(
            [
                lambda: services.verify(
                    manager, p, {"decision": "confirmado", "reason": "Verificado"}
                )
                for _ in range(2)
            ]
        )
        self.assertEqual(sum(r == "conflict" for r in results), 1)
        self.assertEqual(
            Verification.objects.filter(process_id=p, decision="confirmado").count(), 1
        )
