from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from .serializers import JobSerializer
from .permissions import IsCompanyOwner
from .filters import JobFilter
from companies.models import Company


class JobListCreateView(generics.ListCreateAPIView):
    """
    GET → List all active jobs (public)
    POST → Create job (Company only)
    """

    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    filterset_class = JobFilter

    def perform_create(self, serializer):
        """
        Automatically assign job to the logged-in company's profile.
        """
        company = Company.objects.get(owner=self.request.user)
        serializer.save(company=company)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or Delete a job.

    Only company owner can update/delete.
    """

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsCompanyOwner]