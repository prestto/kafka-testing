# celery.py
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_core.settings")

# Create a Celery instance and configure it using the settings from Django.
app = Celery("app_core", broker=settings.CELERY_BROKER_URL)

app.conf.task_default_queue = "default"
# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
