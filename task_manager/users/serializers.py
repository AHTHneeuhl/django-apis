"""
Serializers for user authentication.
"""

from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    """

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        """
        Create user with hashed password.
        """
        return User.objects.create_user(**validated_data)