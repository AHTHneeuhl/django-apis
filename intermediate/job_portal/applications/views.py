from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Application
from .serializers import (
    ApplicantApplicationCreateSerializer,
    ApplicantApplicationListSerializer,
    CompanyApplicationListSerializer,
    ApplicationStatusUpdateSerializer,
)
from .permissions import IsApplicant, IsCompany


# Applicant → Apply
class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicantApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsApplicant]


# Applicant → View own applications
class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicantApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated, IsApplicant]

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).select_related(
            "job", "job__company"
        )


# Company → View applications for their job
class JobApplicationsView(generics.ListAPIView):
    serializer_class = CompanyApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompany]

    def get_queryset(self):
        job_id = self.kwargs["job_id"]
        return Application.objects.filter(
            job__id=job_id,
            job__company__owner=self.request.user
        ).select_related("applicant", "job")


# Company → Update status
class ApplicationStatusUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompany]
    queryset = Application.objects.all()

    def perform_update(self, serializer):
        application = self.get_object()

        # Ensure company owns the job
        if application.job.company.owner != self.request.user:
            raise PermissionDenied("You can update only applications for your jobs.")

        serializer.save()