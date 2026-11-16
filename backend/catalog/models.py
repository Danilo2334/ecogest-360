from django.db import models
from core.models import Owned


class Material(Owned):
    name = models.CharField(max_length=150)
    category = models.CharField(
        max_length=20,
        choices=[(x, x) for x in ["blanco", "verde", "negro", "especial"]],
    )
    active = models.BooleanField(default=True)
