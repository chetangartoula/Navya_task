import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "navya_project.settings")

app = Celery("navya_project")


app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(timezone="Asia/Kathmandu")

app.autodiscover_tasks()
