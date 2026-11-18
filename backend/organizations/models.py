from django.db import models
from django.conf import settings
from core.models import Owned


class Institution(models.Model):
    name = models.CharField(max_length=150)
    active = models.BooleanField(default=True)


class Membership(Owned):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    role = models.CharField(
        max_length=20,
        choices=[(x, x) for x in ["administrador", "gestor", "operador", "consultor"]],
    )


class Site(Owned):
    name = models.CharField(max_length=150)


class Area(Owned):
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
