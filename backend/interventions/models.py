from django.db import models
from django.conf import settings
from core.models import Owned


class Plan(Owned):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_plans"
    )
    problem = models.CharField(max_length=2000)
    action = models.CharField(max_length=2000)
    area = models.ForeignKey("organizations.Area", on_delete=models.PROTECT)
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assigned_plans",
    )
    indicator = models.CharField(max_length=30)
    target = models.DecimalField(max_digits=12, decimal_places=3)
    direction = models.CharField(max_length=10)
    due_date = models.DateField()
    filters = models.JSONField()
    baseline = models.JSONField()
    state = models.CharField(max_length=20, default="borrador")
    version = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(target__gte=0), name="plan_target_nonnegative"
            )
        ]


class Revision(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="revisions")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=2000)
    before = models.JSONField(default=dict)
    after = models.JSONField()


class Followup(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="followups")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2000)


class Evaluation(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="evaluations")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.JSONField()
    version = models.PositiveIntegerField()
