from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
from companies.models import Company
from jobs.models import Job
from applications.models import Application
from accounts.permissions import IsAdminUserRole


class AdminAnalyticsView(APIView):
    """
    Admin-only analytics dashboard endpoint.
    """

    permission_classes = [IsAdminUserRole]

    def get(self, request):

        # 1️⃣ Total counts
        total_users = User.objects.count()
        total_companies = Company.objects.count()
        total_jobs = Job.objects.count()

        # 2️⃣ Applications per job
        applications_per_job = (
            Application.objects
            .values("job__title")
            .annotate(total_applications=Count("id"))
            .order_by("-total_applications")
        )

        # 3️⃣ Most applied company
        most_applied_company = (
            Application.objects
            .values("job__company__name")
            .annotate(total_applications=Count("id"))
            .order_by("-total_applications")
            .first()
        )

        # 4️⃣ Most demanded skill
        # assuming skills is CharField with comma-separated values
        skill_counts = {}

        for job in Job.objects.all():
            skills = job.skills.split(",")
            for skill in skills:
                skill = skill.strip().lower()
                skill_counts[skill] = skill_counts.get(skill, 0) + 1

        most_demanded_skill = (
            max(skill_counts, key=skill_counts.get)
            if skill_counts else None
        )

        return Response({
            "total_users": total_users,
            "total_companies": total_companies,
            "total_jobs": total_jobs,
            "applications_per_job": list(applications_per_job),
            "most_applied_company": most_applied_company,
            "most_demanded_skill": most_demanded_skill,
        })