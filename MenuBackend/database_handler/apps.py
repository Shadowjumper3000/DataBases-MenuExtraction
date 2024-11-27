from django.apps import AppConfig


class DatabaseHandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database_handler'

    def ready(self):
        from .utils import create_database_if_not_exists
        create_database_if_not_exists()