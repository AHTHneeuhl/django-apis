"""
Unit tests for Task model and Task API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from tasks.models import Task

User = get_user_model()


# MODEL TESTS
class TaskModelTest(TestCase):
    """
    Tests for Task model behavior.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

    def test_task_creation(self):
        """
        Ensure task is created with correct fields.
        """
        task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="Test Description",
            completed=False,
        )

        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertFalse(task.completed)
        self.assertEqual(task.user, self.user)
        self.assertIsNotNone(task.created_at)


# API TESTS
class TaskAPITest(APITestCase):
    """
    Tests for Task API endpoints.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="apiuser",
            password="password123"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="password123"
        )

        self.client.force_authenticate(user=self.user)

        self.list_url = reverse("task-list")

    def test_create_task(self):
        """
        Ensure authenticated user can create a task.
        """
        payload = {
            "title": "API Task",
            "description": "API Desc",
            "completed": False
        }

        response = self.client.post(self.list_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().user, self.user)

    def test_list_tasks_returns_only_user_tasks(self):
        """
        Ensure users only see their own tasks.
        """
        Task.objects.create(user=self.user, title="My Task")
        Task.objects.create(user=self.other_user, title="Other Task")

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "My Task")

    def test_user_cannot_access_others_task(self):
        """
        Ensure user cannot retrieve another user's task.
        """
        task = Task.objects.create(user=self.other_user, title="Secret Task")

        detail_url = reverse("task-detail", args=[task.id])
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_cannot_access_tasks(self):
        """
        Ensure unauthenticated access is denied.
        """
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)