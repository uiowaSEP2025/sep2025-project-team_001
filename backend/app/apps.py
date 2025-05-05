from app.utils.multi_bartender_scheduler import MultiBartenderScheduler
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        from app import scheduler_instance

        # Adjust the number of bartenders as needed—here we use 2.
        scheduler_instance.multi_bartender_scheduler = MultiBartenderScheduler(num_bartenders=1)
