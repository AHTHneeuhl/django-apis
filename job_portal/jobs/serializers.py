from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for Job model.
    Company is read-only because it is auto-assigned.
    """

    company = serializers.ReadOnlyField(source="company.name")

    class Meta:
        model = Job
        fields = "__all__"