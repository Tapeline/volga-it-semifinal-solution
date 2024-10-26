from rest_framework.permissions import BasePermission


class IsDoctorOrThatPatient(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return "Doctor" in request.user.roles or obj.pacient_id == request.user.id


class CanEditOrPatientReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return (
            (request.method in ('GET', 'HEAD', 'OPTIONS') and
             obj.pacient_id == request.user.id)
            or
            (
                "Doctor" in request.user.roles or
                "Admin" in request.user.roles or
                "Manager" in request.user.roles
            )
        )


class CanCreateDocument(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (
            "Doctor" in request.user.roles or
            "Admin" in request.user.roles or
            "Manager" in request.user.roles
        )
