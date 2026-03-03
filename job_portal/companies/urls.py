from django.urls import path
from .views import CompanyCreateView, CompanyUpdateView

urlpatterns = [
    path("create/", CompanyCreateView.as_view(), name="company-create"),
    path("<int:pk>/", CompanyUpdateView.as_view(), name="company-detail"),
]