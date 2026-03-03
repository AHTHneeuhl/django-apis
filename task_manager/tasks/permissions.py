"""
Custom permissions for Task app.
"""

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to allow access only to
    the owner of the task.
    """

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check.
        """
        return obj.user == request.user