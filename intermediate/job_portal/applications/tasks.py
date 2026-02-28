from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_application_email(company_email, job_title, candidate_email):
    """
    Send email notification to company when someone applies.
    """

    subject = f"New Application for {job_title}"
    message = f"Candidate {candidate_email} applied for {job_title}"

    send_mail(
        subject,
        message,
        "noreply@jobportal.com",
        [company_email],
        fail_silently=False,
    )