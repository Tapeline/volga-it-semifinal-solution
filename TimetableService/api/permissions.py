from rest_framework.permissions import BasePermission


class HasAdminOrManagerRole(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return ("Admin" in request.user.roles or
                "Manager" in request.user.roles)


class HasAdminOrManagerOrDoctorRole(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return ("Admin" in request.user.roles or
                "Manager" in request.user.roles or
                "Doctor" in request.user.roles)


class HasAdminOrManagerRoleOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return ("Admin" in request.user.roles or
                "Manager" in request.user.roles or
                request.method in ('GET', 'HEAD', 'OPTIONS'))


class CanDeleteThisAppointment(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return ("Admin" in request.user.roles or
                "Manager" in request.user.roles or
                obj.pacient_id == request.user.id)
