from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from .serializers import JobSerializer
from .permissions import IsCompanyOwner
from .documents import JobDocument
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


class JobListView(generics.ListAPIView):
    """
    Public job listing with advanced search, filtering, and ordering.
    """

    serializer_class = JobSerializer
    queryset = Job.objects.filter(is_active=True).select_related("company")

    # Enable filter backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Custom filter class
    filterset_class = JobFilter

    # Search functionality
    search_fields = [
        "title",
        "company__name",
    ]

    # Ordering options
    ordering_fields = [
        "created_at",
        "salary_min",
    ]

    ordering = ["-created_at"]


class JobSearchView(APIView):
    """
    Full-text search using Elasticsearch.
    Searches in:
    - title
    - description
    - skills
    """

    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("q", None)

        if not query:
            return Response({"error": "Search query parameter 'q' required"}, status=400)

        search = JobDocument.search().query(
            "multi_match",
            query=query,
            fields=["title", "description", "skills"],
        )

        response = search.execute()

        results = [hit.meta.id for hit in response]
        jobs = JobDocument.get_queryset().filter(id__in=results)

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)