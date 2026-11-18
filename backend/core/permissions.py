from rest_framework.exceptions import PermissionDenied
from organizations.models import Membership


def member(request, roles=None):
    membership = Membership.objects.filter(
        user=request.user, institution__active=True
    ).first()
    if not membership or (roles and membership.role not in roles):
        raise PermissionDenied("No tienes permiso para esta operación.")
    return membership
