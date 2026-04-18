import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "future_stars.settings")

app = Celery("future_stars")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
