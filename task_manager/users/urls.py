"""
URL configuration for user authentication.
"""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserRegisterView


urlpatterns = [
    # Register new user
    path("register/", UserRegisterView.as_view(), name="register"),

    # Login (get access & refresh token)
    path("login/", TokenObtainPairView.as_view(), name="login"),

    # Refresh access token
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]