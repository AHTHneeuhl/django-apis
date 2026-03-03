from django.db.models import Count
from utils.cache import generate_cache_key
from django.core.cache import cache
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
from companies.models import Company
from jobs.models import Job
from applications.models import Application
from accounts.permissions import IsAdminUserRole


class AdminAnalyticsView(APIView):
    """
    Admin-only analytics dashboard endpoint
    with production-level Redis caching.
    """

    permission_classes = [IsAdminUserRole]

    def get(self, request):

        # Generate query-aware cache key
        cache_key = generate_cache_key("admin_analytics", request)

        # Try cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # -------------------------
        # 1️⃣ Total counts
        # -------------------------
        total_users = User.objects.count()
        total_companies = Company.objects.count()
        total_jobs = Job.objects.count()

        # -------------------------
        # 2️⃣ Applications per job
        # -------------------------
        applications_per_job = (
            Application.objects
            .values("job__title")
            .annotate(total_applications=Count("id"))
            .order_by("-total_applications")
        )

        # -------------------------
        # 3️⃣ Most applied company
        # -------------------------
        most_applied_company = (
            Application.objects
            .values("job__company__name")
            .annotate(total_applications=Count("id"))
            .order_by("-total_applications")
            .first()
        )

        # -------------------------
        # 4️⃣ Most demanded skill
        # -------------------------
        skill_counts = {}

        for job in Job.objects.only("skills"):
            if job.skills:
                skills = job.skills.split(",")
                for skill in skills:
                    skill = skill.strip().lower()
                    skill_counts[skill] = skill_counts.get(skill, 0) + 1

        most_demanded_skill = (
            max(skill_counts, key=skill_counts.get)
            if skill_counts else None
        )

        data = {
            "total_users": total_users,
            "total_companies": total_companies,
            "total_jobs": total_jobs,
            "applications_per_job": list(applications_per_job),
            "most_applied_company": most_applied_company,
            "most_demanded_skill": most_demanded_skill,
        }

        # Store in Redis
        cache.set(
            cache_key,
            data,
            timeout=settings.CACHE_TTL,
        )

        return Response(data)