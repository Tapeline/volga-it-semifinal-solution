from rest_framework.permissions import BasePermission


class HasAdminRole(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return "Admin" in request.user.roles
