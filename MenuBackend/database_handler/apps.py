from django.apps import AppConfig
from django.core.management import call_command
import MySQLdb
from django.conf import settings


class DatabaseHandlerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "database_handler"

    def ready(self):
        self.create_database_if_not_exists()
        self.run_migrations()

    def create_database_if_not_exists(self):
        try:
            connection = MySQLdb.connect(
                host=settings.DATABASES["default"]["HOST"],
                user=settings.DATABASES["default"]["USER"],
                passwd=settings.DATABASES["default"]["PASSWORD"],
                port=int(settings.DATABASES["default"]["PORT"]),
            )
            cursor = connection.cursor()
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {settings.DATABASES['default']['NAME']}"
            )
            cursor.close()
            connection.close()
            print(
                f"Database {settings.DATABASES['default']['NAME']} created or already exists."
            )
        except MySQLdb.Error as e:
            print(f"Error creating database: {e}")

    def run_migrations(self):
        try:
            call_command("makemigrations", interactive=False)
            call_command("migrate", interactive=False)
        except Exception as e:
            print(f"Error running migrations: {e}")
