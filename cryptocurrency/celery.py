from __future__ import absolute_import
from datetime import timedelta
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cryptocurrency.settings")
from django.conf import settings  # noqa

app = Celery("cryptocurrency.tasks")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "add-every-5-seconds": {
        "task": "api.tasks.tasks.add",
        "schedule": timedelta(seconds=5),
    },
    "test_exposed": {
        "task": "api.tasks.tasks.test",
        "schedule": timedelta(seconds=30),  # This is exposed via API.
    },
    "get_daily": {
        "task": "api.tasks.tasks.daily",
        "schedule": crontab(hour="23", minute="59"),  # Execute everyday at 23:59
    },
    "get_weekly": {
        "task": "api.tasks.tasks.weekly",
        "schedule": crontab(
            hour="23", minute="59", day_of_week="sun"
        ),  # Execute every sunday ay 23:59
    },
    "get_monthly": {
        "task": "api.tasks.tasks.monthly",
        "schedule": crontab(
            0, 0, day_of_month="1"
        ),  # Execute on the first day of every month.
    },
}

app.conf.timezone = "UTC"
