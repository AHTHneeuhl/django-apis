from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Application
from .tasks import send_application_email
from .serializers import (
    ApplicantApplicationCreateSerializer,
    ApplicantApplicationListSerializer,
    CompanyApplicationListSerializer,
    ApplicationStatusUpdateSerializer,
)
from .permissions import IsApplicant, IsCompany


# Applicant → Apply
class ApplicationCreateView(generics.CreateAPIView):
    """
    Candidate applies to a job.
    """

    queryset = Application.objects.all()
    serializer_class = ApplicantApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save application and trigger background email.
        """

        job = serializer.validated_data["job"]

        application = serializer.save(candidate=self.request.user)

        # Trigger Celery task AFTER save
        send_application_email.delay(
            company_email=job.company.owner.email,
            job_title=job.title,
            candidate_email=self.request.user.email,
        )


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

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Filtering
    filterset_fields = ["status"]

    # Ordering
    ordering_fields = ["applied_at", "status"]
    ordering = ["-applied_at"]

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