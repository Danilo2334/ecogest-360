from django.test import TransactionTestCase
from django.db import connection
from tests.fixtures import Fixture
from waste.models import Generation
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class PersistenceTests(Fixture, TransactionTestCase):
    def test_committed_data_survives_new_connection_and_session(self):
        g = self.generation()
        connection.close()
        self.assertEqual(Generation.objects.get(pk=g).kg, 25)
        client = APIClient()
        client.force_authenticate(User.objects.get(pk=self.operator.pk))
        response = client.get(f"/api/generations/{g}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["provenance"], "simulado")
