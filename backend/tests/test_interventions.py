from django.test import TestCase
from tests.fixtures import Fixture
from django.utils import timezone
from datetime import timedelta
from waste.models import Generation
from interventions.models import Plan
from organizations.models import Institution


class InterventionTests(Fixture, TestCase):
    def test_evaluation_preserves_base_and_does_not_claim_causality(self):
        self.generation()
        Generation.objects.update(date="2026-11-13T10:00:00-05:00")
        self.client.force_authenticate(self.manager)
        payload = self.payload()
        payload["filters"].update(
            generated_from="2026-11-13", generated_to="2026-11-13"
        )
        p = self.post("v2/plans", payload).data
        for state in ["en_curso", "en_evaluacion"]:
            p = self.post(
                f'v2/plans/{p["id"]}/transitions',
                {"version": p["version"], "state": state, "reason": "Ensayo"},
            ).data
        Generation.objects.create(
            institution=self.institution,
            area=self.area,
            material=self.material,
            actor=self.operator,
            kg="18",
            provenance="simulado",
            date="2026-11-14T10:00:00-05:00",
            method="Prueba",
        )
        result = self.post(
            f'v2/plans/{p["id"]}/evaluations',
            {
                "version": p["version"],
                "reason": "Comparación",
                "generated_from": "2026-11-14",
                "generated_to": "2026-11-14",
            },
        )
        self.assertEqual(result.status_code, 201, result.data)
        p = result.data
        self.assertEqual(p["evaluations"][-1]["status"], "alcanzada")
        self.assertEqual(p["baseline"]["value"], "25.000")
        changed = self.client.patch(
            f'/api/v2/plans/{p["id"]}',
            {"version": p["version"], "reason": "Meta más exigente", "target": "10"},
            format="json",
        ).data
        self.assertEqual(
            self.post(
                f'v2/plans/{p["id"]}/transitions',
                {
                    "version": changed["version"],
                    "reason": "Intento sin reevaluar",
                    "state": "cerrado",
                },
            ).status_code,
            400,
        )
        Generation.objects.filter(date__date="2026-11-13").update(kg="26")
        result = self.post(
            f'v2/plans/{p["id"]}/evaluations',
            {
                "version": changed["version"],
                "reason": "Revisar cambio de fuente",
                "generated_from": "2026-11-14",
                "generated_to": "2026-11-14",
            },
        )
        self.assertEqual(result.data["evaluations"][-1]["status"], "no_evaluable")
        closed = self.post(
            f'v2/plans/{p["id"]}/transitions',
            {
                "version": result.data["version"],
                "reason": "Cierre con límite explícito",
                "state": "cerrado",
            },
        )
        self.assertEqual(closed.status_code, 201)

    def test_idempotency_and_other_institution(self):
        self.generation()
        self.client.force_authenticate(self.manager)
        first = self.post("v2/plans", self.payload(), key="plan-retry")
        second = self.post("v2/plans", self.payload(), key="plan-retry")
        self.assertEqual(first.data["id"], second.data["id"])
        self.assertEqual(Plan.objects.count(), 1)
        Plan.objects.filter(pk=first.data["id"]).update(
            institution=Institution.objects.create(name="Otra")
        )
        self.assertEqual(self.client.get("/api/v2/plans").data, [])
        self.assertEqual(
            self.client.patch(
                f'/api/v2/plans/{first.data["id"]}',
                {"version": 1, "reason": "Ajeno", "target": "1"},
                format="json",
            ).status_code,
            404,
        )

    def payload(self):
        return dict(
            problem="Masa pendiente de tratamiento",
            action="Revisar separación y evidencias",
            area=self.area.pk,
            responsible=self.operator.pk,
            indicator="generated",
            target="20",
            direction="reduce",
            due_date=str(timezone.localdate() + timedelta(days=30)),
            filters={
                "area": str(self.area.pk),
                "provenance": "simulado",
                "generated_from": "2026-11-15",
                "generated_to": "2026-11-15",
            },
            reason="Creación académica simulada",
        )

    def create_plan(self):
        self.generation()
        self.client.force_authenticate(self.manager)
        r = self.post("v2/plans", self.payload())
        self.assertEqual(r.status_code, 201, r.data)
        return r.data

    def test_only_manager_and_revision_conflict(self):
        self.generation()
        self.assertEqual(self.post("v2/plans", self.payload()).status_code, 403)
        from django.contrib.auth.models import User
        from organizations.models import Membership

        admin = User.objects.create_user("plan_admin")
        Membership.objects.create(
            user=admin, institution=self.institution, role="administrador"
        )
        self.client.force_authenticate(admin)
        self.assertEqual(self.post("v2/plans", self.payload()).status_code, 403)
        self.client.force_authenticate(self.manager)
        r = self.post("v2/plans", self.payload())
        self.assertEqual(r.status_code, 201)
        p = r.data
        edit = {
            "version": p["version"],
            "reason": "Ajustar meta revisada",
            "target": "19",
        }
        result = self.client.patch(f'/api/v2/plans/{p["id"]}', edit, format="json")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            self.client.patch(
                f'/api/v2/plans/{p["id"]}', edit, format="json"
            ).status_code,
            409,
        )
        self.assertEqual(len(result.data["revisions"]), 2)
        self.operator.is_active = False
        self.operator.save()
        self.assertFalse(self.client.get("/api/v2/plans").data[0]["responsible_active"])
        self.client.force_authenticate(self.reader)
        self.assertEqual(self.client.get("/api/v2/plans").status_code, 200)
        self.assertEqual(
            self.client.patch(
                f'/api/v2/plans/{p["id"]}', edit, format="json"
            ).status_code,
            403,
        )

    def test_state_and_missing_evidence_do_not_claim_success(self):
        p = self.create_plan()
        for state in ["en_curso", "en_evaluacion"]:
            r = self.post(
                f'v2/plans/{p["id"]}/transitions',
                {
                    "version": p["version"],
                    "state": state,
                    "reason": "Revisión humana simulada",
                },
            )
            self.assertEqual(r.status_code, 201, r.data)
            p = r.data
        r = self.post(
            f'v2/plans/{p["id"]}/transitions',
            {
                "version": p["version"],
                "state": "cerrado",
                "reason": "Intento sin evaluación",
            },
        )
        self.assertEqual(r.status_code, 400)
        r = self.post(
            f'v2/plans/{p["id"]}/evaluations',
            {
                "version": p["version"],
                "generated_from": "2026-11-15",
                "generated_to": "2026-11-15",
                "reason": "Período solapado",
            },
        )
        self.assertEqual(r.status_code, 400)

    def test_invalid_assignment_and_universe(self):
        self.generation()
        self.client.force_authenticate(self.manager)
        data = self.payload()
        data["responsible"] = 999999
        self.assertEqual(self.post("v2/plans", data).status_code, 400)
        data = self.payload()
        data["filters"]["area"] = "999999"
        self.assertEqual(self.post("v2/plans", data).status_code, 400)
