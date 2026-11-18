import hashlib
import json
from django.db import transaction, connection
from rest_framework.exceptions import ValidationError
from core.models import OperationReceipt
from core.errors import Conflict


def execute(membership, operation, key, payload, action):
    if not key or len(key) > 100:
        raise ValidationError("Se requiere Idempotency-Key (máximo 100 caracteres).")
    normalized = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False)
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    identity = f"{membership.institution_id}:{membership.user_id}:{operation}:{key}"
    lock = int.from_bytes(
        hashlib.sha256(identity.encode()).digest()[:8], "big", signed=True
    )
    with transaction.atomic():
        # Serializes retries before querying the receipt, across processes and connections.
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_xact_lock(%s)", [lock])
        old = OperationReceipt.objects.filter(
            institution=membership.institution,
            actor=membership.user,
            operation=operation,
            key=key,
        ).first()
        if old:
            if old.digest != digest:
                raise Conflict("La clave de operación ya fue usada con otro contenido.")
            return old.result
        result = action()
        OperationReceipt.objects.create(
            institution=membership.institution,
            actor=membership.user,
            operation=operation,
            key=key,
            digest=digest,
            result=result,
        )
        return result
