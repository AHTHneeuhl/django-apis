from django.db import models
from django.conf import settings
from companies.models import Company


class Job(models.Model):
    """
    Job model created by a company.
    Each job belongs to a company.
    """

    class JobType(models.TextChoices):
        INTERNSHIP = "INTERNSHIP", "Internship"
        FULL_TIME = "FULL_TIME", "Full Time"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs",
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    # Skills stored as comma-separated text (can later improve to M2M)
    skills_required = models.CharField(max_length=500)

    location = models.CharField(max_length=255)

    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)

    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices,
    )

    deadline = models.DateField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title