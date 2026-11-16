from django.db import models
from django.conf import settings
from core.models import Owned


class Generation(Owned):
    area = models.ForeignKey("organizations.Area", on_delete=models.PROTECT)
    material = models.ForeignKey("catalog.Material", on_delete=models.PROTECT)
    kg = models.DecimalField(max_digits=12, decimal_places=3)
    date = models.DateTimeField()
    provenance = models.CharField(
        max_length=20, choices=[(x, x) for x in ["medido", "estimado", "simulado"]]
    )
    method = models.CharField(max_length=500, blank=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    reviewed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(kg__gt=0), name="generation_positive"
            )
        ]
        indexes = [models.Index(fields=["institution", "date"])]
