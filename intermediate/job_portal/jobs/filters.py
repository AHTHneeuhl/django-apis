import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    """
    Advanced filtering for job listing.
    """

    location = django_filters.CharFilter(lookup_expr="icontains")
    job_type = django_filters.CharFilter(lookup_expr="iexact")
    salary_min = django_filters.NumberFilter(field_name="salary_min", lookup_expr="gte")
    salary_max = django_filters.NumberFilter(field_name="salary_max", lookup_expr="lte")
    company = django_filters.CharFilter(field_name="company__name", lookup_expr="icontains")
    skills = django_filters.CharFilter(field_name="skills_required", lookup_expr="icontains")

    class Meta:
        model = Job
        fields = [
            "location",
            "job_type",
            "salary_min",
            "salary_max",
            "company",
            "skills",
        ]