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