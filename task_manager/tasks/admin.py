"""
Admin configuration for Task model.

This file customizes how the Task model appears
inside Django Admin panel.
"""

from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Task model.
    """

    # Fields displayed in the admin list view
    list_display = (
        "id",
        "title",
        "user",
        "completed",
        "due_date",
        "created_at",
    )

    # Sidebar filters for quick filtering
    list_filter = (
        "completed",
        "due_date",
        "created_at",
    )

    # Search functionality in admin
    search_fields = (
        "title",
        "description",
        "user__username",
    )

    # Default ordering (newest first)
    ordering = ("-created_at",)