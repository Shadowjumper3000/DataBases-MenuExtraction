from django.apps import AppConfig
from django.core.management import call_command


class DatabaseHandlerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "database_handler"

    def ready(self):
        from .utils import create_database_if_not_exists

        create_database_if_not_exists()
        # Run migrations to create tables
        try:
            call_command("makemigrations", interactive=False)
            call_command("migrate", interactive=False)
        except Exception as e:
            print(f"Error running migrations: {e}")
            pass
