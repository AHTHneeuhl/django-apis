from django.db import models
from django.conf import settings


class Company(models.Model):
    """
    Company profile model.

    Each company profile is owned by a user with COMPANY role.
    One-to-One relationship ensures:
    - One company user → One company profile
    """

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_profile",
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)

    # Logo image will be stored inside media/company_logos/
    logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name