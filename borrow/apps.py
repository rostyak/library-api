import os

from django.apps import AppConfig


class BorrowConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "borrow"

    def ready(self):
        print("Starting scheduler...")
        from .scheduled_tasks import schedule_message
        if os.environ.get('RUN_MAIN'):
            schedule_message()
