from rest_framework.permissions import BasePermission


class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "COMPANY"


class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "CANDIDATE"


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN"


class IsAdminUserRole(BasePermission):
    """
    Allows access only to users with ADMIN role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"