from rest_framework.permissions import BasePermission


class HasAdminRoleOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (
            (request.method in ('GET', 'HEAD', 'OPTIONS'))
            or
            ("Admin" in request.user.roles)
        )
