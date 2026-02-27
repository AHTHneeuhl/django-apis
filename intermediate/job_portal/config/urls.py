from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import RegisterView


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/companies/", include("companies.urls")),
    path("api/jobs/", include("jobs.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)