from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from organizations.models import Institution, Membership, Site, Area
from catalog.models import Material


class Fixture:
    def setUp(self):
        self.institution = Institution.objects.create(name="Piloto de prueba")
        site = Site.objects.create(institution=self.institution, name="Campus")
        self.area = Area.objects.create(
            institution=self.institution, site=site, name="Cafetería"
        )
        self.material = Material.objects.create(
            institution=self.institution, name="Orgánicos", category="verde"
        )
        self.operator = User.objects.create_user(
            "operador", password="Test-only-pass-123!"
        )
        self.manager = User.objects.create_user(
            "gestor", password="Test-only-pass-123!"
        )
        self.reader = User.objects.create_user(
            "consultor", password="Test-only-pass-123!"
        )
        for user, role in [
            (self.operator, "operador"),
            (self.manager, "gestor"),
            (self.reader, "consultor"),
        ]:
            Membership.objects.create(
                user=user, institution=self.institution, role=role
            )
        self.client = APIClient()
        self.client.force_authenticate(self.operator)

    def post(self, path, data, key=None):
        import uuid

        return self.client.post(
            "/api/" + path,
            data,
            format="json",
            HTTP_IDEMPOTENCY_KEY=key or str(uuid.uuid4()),
        )

    def generation(self, kg="25.000"):
        response = self.post(
            "generations",
            {
                "area": self.area.id,
                "material": self.material.id,
                "kg": kg,
                "unit": "kg",
                "provenance": "simulado",
                "date": "2026-11-15T10:00:00-05:00",
                "method": "Demo",
            },
        )
        self.assertEqual(response.status_code, 201, response.data)
        return response.data["id"]

    def lot(self):
        g = self.generation()
        response = self.post("lots", {"sources": [{"generation": g, "kg": "25.000"}]})
        self.assertEqual(response.status_code, 201, response.data)
        return response.data["id"], g
