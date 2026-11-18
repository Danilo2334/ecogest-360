import uuid
from django.db import models
from django.conf import settings
from core.models import Owned


class Lot(Owned):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    provenance = models.CharField(max_length=20)
    closed = models.BooleanField(default=False)

    def available(self):
        from decimal import Decimal

        assigned = self.allocations.aggregate(v=models.Sum("kg"))["v"] or Decimal("0")
        consumed = self.movements.exclude(type="logistico").aggregate(
            v=models.Sum("kg")
        )["v"] or Decimal("0")
        return assigned - consumed


class Allocation(models.Model):
    generation = models.ForeignKey(
        "waste.Generation", on_delete=models.PROTECT, related_name="allocations"
    )
    lot = models.ForeignKey(Lot, on_delete=models.PROTECT, related_name="allocations")
    kg = models.DecimalField(max_digits=12, decimal_places=3)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(kg__gt=0), name="allocation_positive"
            )
        ]


class Movement(Owned):
    lot = models.ForeignKey(Lot, on_delete=models.PROTECT, related_name="movements")
    type = models.CharField(
        max_length=30,
        choices=[(x, x) for x in ["logistico", "entrega", "entrada_compostaje"]],
    )
    kg = models.DecimalField(max_digits=12, decimal_places=3)
    destination = models.CharField(max_length=500)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(kg__gt=0), name="movement_positive"
            )
        ]


class ConsumptionSource(models.Model):
    movement = models.ForeignKey(
        Movement, on_delete=models.PROTECT, related_name="sources"
    )
    allocation = models.ForeignKey(
        Allocation, on_delete=models.PROTECT, related_name="consumptions"
    )
    kg = models.DecimalField(max_digits=12, decimal_places=3)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(kg__gt=0), name="source_positive")
        ]
