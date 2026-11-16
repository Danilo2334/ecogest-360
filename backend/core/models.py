from django.db import models
from django.conf import settings


class Owned(models.Model):
    institution = models.ForeignKey(
        "organizations.Institution", on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AuditEvent(Owned):
    entity = models.CharField(max_length=100)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    reason = models.CharField(max_length=2000)
    before = models.JSONField(default=dict)
    after = models.JSONField(default=dict)


class Incident(Owned):
    entity = models.CharField(max_length=100)
    reason = models.CharField(max_length=2000)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    state = models.CharField(max_length=20, default="pendiente")


class OperationReceipt(Owned):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    operation = models.CharField(max_length=200)
    key = models.CharField(max_length=100)
    digest = models.CharField(max_length=64)
    result = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "actor", "operation", "key"],
                name="unique_operation_receipt",
            )
        ]
