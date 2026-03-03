from rest_framework.permissions import BasePermission


class IsCompanyRole(BasePermission):
    """
    Allows access only to users with COMPANY role.
    """

    def has_permission(self, request, view):
        return request.user.role == "COMPANY"


class IsOwner(BasePermission):
    """
    Object-level permission.
    Only allow users to edit their own company profile.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user