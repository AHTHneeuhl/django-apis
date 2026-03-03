from rest_framework import serializers
from django.utils import timezone
from .models import Application
from .validators import validate_file_size


class ApplicantApplicationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used by APPLICANT to apply for a job.
    """

    class Meta:
        model = Application
        fields = ["job", "resume", "cover_letter"]

    def validate(self, attrs):
        user = self.context["request"].user
        job = attrs.get("job")

        # Ensure user is applicant
        if user.role != "APPLICANT":
            raise serializers.ValidationError("Only applicants can apply to jobs.")

        # Prevent applying to inactive job
        if not job.is_active:
            raise serializers.ValidationError("Cannot apply to inactive job.")

        # Prevent applying after deadline
        if job.deadline and job.deadline < timezone.now().date():
            raise serializers.ValidationError("Job deadline has passed.")

        return attrs

    def validate_resume(self, value):
        validate_file_size(value)
        return value

    def create(self, validated_data):
        return Application.objects.create(
            applicant=self.context["request"].user,
            **validated_data
        )


class ApplicantApplicationListSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    company_name = serializers.CharField(source="job.company.name", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "job_title",
            "company_name",
            "status",
            "applied_at",
        ]


class CompanyApplicationListSerializer(serializers.ModelSerializer):
    applicant_email = serializers.CharField(source="applicant.email", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "applicant_email",
            "resume",
            "cover_letter",
            "status",
            "applied_at",
        ]


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Used by COMPANY to update application status only.
    """

    class Meta:
        model = Application
        fields = ["status"]