from decimal import Decimal, InvalidOperation
from django.utils.dateparse import parse_datetime, parse_date
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


def mass(data):
    if data.get("unit") != "kg":
        raise ValidationError("La unidad debe ser kg.")
    try:
        value = Decimal(str(data.get("kg", "")))
    except (InvalidOperation, ValueError):
        raise ValidationError("Peso inválido.")
    if (
        not value.is_finite()
        or value <= 0
        or value >= Decimal("1000000000")
        or value.as_tuple().exponent < -3
    ):
        raise ValidationError(
            "Peso positivo, hasta 3 decimales y menor a 1 000 000 000 kg."
        )
    return value


def text(data, key, max_length=150):
    value = str(data.get(key, "")).strip()
    if not value or len(value) > max_length:
        raise ValidationError(
            f"{key}: campo obligatorio, máximo {max_length} caracteres."
        )
    return value


def provenance(data):
    value = data.get("provenance")
    if value not in ["medido", "estimado", "simulado"]:
        raise ValidationError("Procedencia inválida.")
    return value


def date_time(data, key="date"):
    try:
        value = parse_datetime(str(data.get(key, "")))
    except ValueError:
        value = None
    if value is None or timezone.is_naive(value):
        raise ValidationError("Fecha y hora con zona requeridas.")
    return value


def scoped(model, membership, pk, lock=False):
    query = model.objects.filter(institution=membership.institution)
    if lock:
        query = query.select_for_update()
    try:
        return get_object_or_404(query, pk=pk)
    except (ValueError, TypeError):
        raise ValidationError("Identificador inválido.")


def kg(value):
    return format(value, ".3f")
