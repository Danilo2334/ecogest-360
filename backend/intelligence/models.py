from django.conf import settings
from django.db import models


class Invocation(models.Model):
    """Only accounting metadata. Never prompts, answers, names or provider errors."""

    institution = models.ForeignKey(
        "organizations.Institution", on_delete=models.PROTECT
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    key = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    day = models.DateField()
    status = models.CharField(max_length=12, default="pending")
    model = models.CharField(max_length=80)
    debit = models.DecimalField(max_digits=14, decimal_places=8)
    input_tokens = models.PositiveIntegerField(null=True)
    output_tokens = models.PositiveIntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "key"], name="assistant_user_key_unique"
            ),
            models.CheckConstraint(
                condition=models.Q(debit__gte=0), name="assistant_nonnegative_debit"
            ),
        ]
