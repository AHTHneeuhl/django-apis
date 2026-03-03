from rest_framework.permissions import BasePermission


class IsCompanyOwner(BasePermission):
    """
    Only allow company owners to modify their own jobs.
    """

    def has_object_permission(self, request, view, obj):
        return obj.company.owner == request.user