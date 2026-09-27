from rest_framework.permissions import BasePermission

from .models import Company


class IsAdminUser(BasePermission):
    """
    Grants access only to companies whose role is ADMIN.
    """

    message = "Admin access required."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        company = getattr(request.user, 'company', None)
        if company is None:
            return False
        return company.role == Company.Role.ADMIN
