import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


app = Celery("core")
app.config_from_object("django.conf:settings")
app.conf.broker_url = settings.CELERY_BROKER_URL

# Configure Celery Beat
app.conf.beat_schedule = {
    "add_users_to_private_group": {
        "task": "subscription_service.tasks.find_new_subscriptions",
        "schedule": 10.0,
    },
    "delete_subscription": {
        "task": "subscription_service.tasks.delete_expired_subscriptions",
        "schedule": 10.0,
    },
}

app.autodiscover_tasks()
