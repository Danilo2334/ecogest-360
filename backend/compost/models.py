from django.db import models
from django.conf import settings
from core.models import Owned


class Process(Owned):
    provenance = models.CharField(max_length=20)
    state = models.CharField(max_length=20, default="en_proceso")
    observations = models.TextField(blank=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class Input(models.Model):
    process = models.ForeignKey(
        Process, on_delete=models.PROTECT, related_name="inputs"
    )
    movement = models.OneToOneField(
        "traceability.Movement", on_delete=models.PROTECT, related_name="compost_input"
    )


class Output(Owned):
    process = models.OneToOneField(
        Process, on_delete=models.PROTECT, related_name="output"
    )
    kg = models.DecimalField(max_digits=12, decimal_places=3)
    provenance = models.CharField(max_length=20)
    destination = models.CharField(max_length=500)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(kg__gt=0), name="output_positive")
        ]


class Measurement(Owned):
    process = models.ForeignKey(
        Process, on_delete=models.PROTECT, related_name="measurements"
    )
    value = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.CharField(max_length=30)
    type = models.CharField(max_length=50)
    date = models.DateTimeField()
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class Evidence(Owned):
    process = models.ForeignKey(
        Process, on_delete=models.PROTECT, related_name="evidences"
    )
    receiver = models.CharField(max_length=150)
    date = models.DateField()
    description = models.CharField(max_length=2000)
    reference = models.CharField(max_length=500, blank=True)
    file = models.FileField(upload_to="evidence/%Y/%m/", blank=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class Verification(Owned):
    process = models.ForeignKey(
        Process, on_delete=models.PROTECT, related_name="verifications"
    )
    decision = models.CharField(max_length=20)
    reason = models.CharField(max_length=2000)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["process"],
                condition=models.Q(decision="confirmado"),
                name="one_process_confirmation",
            )
        ]
