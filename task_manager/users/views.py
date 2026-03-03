"""
User authentication views.
"""

from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []