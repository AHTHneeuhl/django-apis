"""
Serializers for Task app.

Serializers convert model instances to JSON
and validate incoming JSON data.
"""

from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    Handles conversion between Task model and JSON representation.
    """

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "completed",
            "due_date",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "created_at", "updated_at"]