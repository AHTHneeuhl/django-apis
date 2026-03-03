from django.urls import path
from .views import (
    ApplicationCreateView,
    MyApplicationsView,
    JobApplicationsView,
    ApplicationStatusUpdateView,
)

urlpatterns = [
    path("", ApplicationCreateView.as_view(), name="apply"),
    path("my/", MyApplicationsView.as_view(), name="my_applications"),
    path("job/<int:job_id>/", JobApplicationsView.as_view(), name="job_applications"),
    path("<int:pk>/status/", ApplicationStatusUpdateView.as_view(), name="update_status"),
]