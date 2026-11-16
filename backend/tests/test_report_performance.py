from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
from decimal import Decimal
from django.test import TransactionTestCase
from django.db import connection, close_old_connections
from django.utils import timezone
from tests.fixtures import Fixture
from django.test import TestCase
from organizations.models import Membership
from waste.models import Generation
from reports.selectors import report
from reports.csv_export import export


class PerformanceTests(TransactionTestCase):
    setUp = Fixture.setUp

    def test_ten_thousand_rows_ten_readers(self):
        Generation.objects.bulk_create(
            [
                Generation(
                    institution=self.institution,
                    area=self.area,
                    material=self.material,
                    kg=Decimal("1"),
                    provenance="simulado",
                    date=timezone.now(),
                    actor=self.operator,
                )
                for _ in range(10000)
            ],
            batch_size=1000,
        )

        def worker(_):
            close_old_connections()
            try:
                m = Membership.objects.get(user_id=self.operator.id)
                from rest_framework.test import APIClient

                client = APIClient()
                client.force_authenticate(m.user)
                started = perf_counter()
                response = client.get("/api/dashboard")
                result = response.data
                self.assertEqual(response.status_code, 200)
                self.assertEqual(result["generated"], "10000.000")
                return perf_counter() - started
            finally:
                connection.close()

        with ThreadPoolExecutor(max_workers=10) as pool:
            times = list(pool.map(worker, range(10)))
        p95 = max(times)
        m = Membership.objects.get(user=self.operator)
        started = perf_counter()
        context, rows = report(m, {})
        response = export(context, rows)
        duration = perf_counter() - started
        self.assertGreater(len(response.content), 10000)
        print(
            f"PERFORMANCE: 10000 registros, 10 lectores, p95 conservador={p95:.3f}s; CSV={duration:.3f}s"
        )
        self.assertLess(p95, 2.0)
        self.assertLess(duration, 10.0)
