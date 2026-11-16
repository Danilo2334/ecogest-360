import io
import json
from unittest.mock import patch
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.contrib.auth.models import User
from organizations.models import Institution, Membership
from waste.models import Generation
from core.models import AuditEvent, OperationReceipt
from reports.observatory import observatory


class ObservatoryDemoTests(TestCase):
    def test_plan_receipts_do_not_invalidate_environmental_seed(self):
        first=self.run_seed('--apply','--end-date','2026-11-15')
        m=Membership.objects.get(user__username='intelligence_gestor')
        OperationReceipt.objects.create(institution=m.institution,actor=m.user,operation='v2/plans',key='demo-plan',digest='test',result={'id':1})
        self.assertEqual(first,self.run_seed('--describe'))

    def run_seed(self, *args):
        out = io.StringIO()
        with patch.dict("os.environ", {"DEMO_PASSWORD": "Only-test-password-123!"}):
            call_command("seed_observatory_demo", *args, stdout=out)
        return json.loads(out.getvalue())

    def test_dry_run_writes_nothing(self):
        self.run_seed()
        self.assertEqual(Institution.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)

    def test_repeat_is_isolated_and_preserves_data(self):
        original = Institution.objects.create(name="Institución anterior")
        first = self.run_seed("--apply", "--end-date", "2026-11-15")
        ids = list(Generation.objects.values_list("id", flat=True))
        events = AuditEvent.objects.count()
        again = self.run_seed("--apply", "--end-date", "2026-11-15")
        self.assertEqual(first, again)
        self.assertEqual(ids, list(Generation.objects.values_list("id", flat=True)))
        self.assertEqual(events, AuditEvent.objects.count())
        self.assertTrue(
            Institution.objects.filter(pk=original.pk, name=original.name).exists()
        )
        self.assertEqual(Generation.objects.count(), 84)
        self.assertFalse(Generation.objects.exclude(provenance="simulado").exists())
        self.assertEqual(Generation.objects.values("institution").distinct().count(), 1)
        m = Membership.objects.get(user__username="intelligence_gestor")
        d = observatory(
            m,
            {
                "provenance": "simulado",
                "generated_from": first["current_from"],
                "generated_to": first["current_to"],
            },
        )
        self.assertTrue(d["comparison"]["available"])
        self.assertEqual(len(d["series"]), 14)
        self.assertEqual(len(d["areas"]), 3)
        self.assertEqual(d["summary"]["generated"], "365.000")
        self.assertEqual(d["summary"]["verified_compost"], "100.000")
        self.assertEqual(d["summary"]["pending"], "265.000")
        self.assertEqual(d["comparison"]["previous_generated"], "281.000")
        filtered = observatory(
            m,
            {
                "provenance": "simulado",
                "generated_from": first["current_from"],
                "generated_to": first["current_to"],
                "area": str(d["areas"][0]["id"]),
            },
        )
        self.assertEqual(filtered["summary"]["generated"], "187.000")
        self.assertEqual(filtered["summary"]["pending"], "87.000")

    def test_collision_does_not_adopt_account(self):
        user = User.objects.create_user("intelligence_gestor")
        with self.assertRaises(CommandError):
            self.run_seed("--apply")
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(pk=user.pk).exists())
        self.assertEqual(Institution.objects.count(), 0)

    def test_modified_cohort_is_not_repaired(self):
        self.run_seed("--apply", "--end-date", "2026-11-15")
        g = Generation.objects.first()
        Generation.objects.filter(pk=g.pk).update(method="Cambio posterior")
        with self.assertRaises(CommandError):
            self.run_seed("--apply", "--end-date", "2026-11-15")
        g.refresh_from_db()
        self.assertEqual(g.method, "Cambio posterior")
