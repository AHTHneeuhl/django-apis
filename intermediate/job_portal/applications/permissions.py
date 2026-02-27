from rest_framework.permissions import BasePermission


class IsApplicant(BasePermission):
    """
    Allows access only to users with APPLICANT role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "APPLICANT"


class IsCompany(BasePermission):
    """
    Allows access only to users with COMPANY role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "COMPANY"