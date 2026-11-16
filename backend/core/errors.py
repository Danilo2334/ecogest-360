from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.views import exception_handler
from django.http import JsonResponse


def csrf_failure(request, reason=""):
    return JsonResponse(
        {
            "code": "403",
            "message": "La sesión de seguridad cambió. Actualiza la página e intenta de nuevo.",
        },
        status=403,
    )


class Conflict(APIException):
    status_code = 409
    default_detail = "Conflicto de saldo o estado."
    default_code = "conflict"


def handler(exc, context):
    if isinstance(exc, ModelValidationError):
        exc = ValidationError(
            exc.message_dict if hasattr(exc, "message_dict") else exc.messages
        )
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "code": str(response.status_code),
            "message": str(getattr(exc, "detail", exc)),
            "field_errors": response.data,
        }
    return response
