import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("job_portal")

# Read settings from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto discover tasks.py in apps
app.autodiscover_tasks()