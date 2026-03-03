"""
API views for Task app.
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner


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
    permission_classes = [IsAuthenticated, IsOwner]

    # Enable filtering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields for exact filtering
    filterset_fields = ["completed", "due_date"]

    # Search functionality
    search_fields = ["title", "description"]

    # Ordering
    ordering_fields = ["created_at", "due_date"]
    ordering = ["-created_at"]  # Default ordering

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