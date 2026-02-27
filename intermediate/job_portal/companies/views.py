from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializers import CompanySerializer
from .permissions import IsCompanyRole, IsOwner


class CompanyCreateView(generics.CreateAPIView):
    """
    Create company profile.

    Only users with COMPANY role can create profile.
    Automatically assigns logged-in user as owner.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyRole]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CompanyUpdateView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update company profile.

    Only:
    - COMPANY role
    - Owner of that company
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyRole, IsOwner]