"""
API views for Task app.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Task model.

    Endpoints automatically generated:
    - GET /tasks/
    - POST /tasks/
    - GET /tasks/{id}/
    - PUT /tasks/{id}/
    - PATCH /tasks/{id}/
    - DELETE /tasks/{id}/
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return tasks belonging only to the authenticated user.
        """
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user
        when creating a new task.
        """
        serializer.save(user=self.request.user)