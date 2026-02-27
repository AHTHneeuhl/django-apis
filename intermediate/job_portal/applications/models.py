from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from jobs.models import Job


class Application(models.Model):
    """
    Represents a job application submitted by an APPLICANT
    to a specific job.
    """

    class StatusChoices(models.TextChoices):
        APPLIED = "APPLIED", "Applied"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    # Applicant who applied
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    # Job being applied to
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    # Resume upload (PDF only)
    resume = models.FileField(
        upload_to="resumes/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    # Optional cover letter
    cover_letter = models.TextField(blank=True, null=True)

    # Current application status
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.APPLIED,
    )

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Prevent duplicate applications
        constraints = [
            models.UniqueConstraint(
                fields=["applicant", "job"],
                name="unique_application_per_job",
            )
        ]
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.applicant.email} → {self.job.title}"