from django.core.management import BaseCommand
from django.db import connection
from django.apps import apps
from django.conf import settings

class Command(BaseCommand):
    help = 'Reset Database tables and sequences for the api testing'

    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            self.stdout.write(
                self.style.ERROR('This command can only be run in DEBUG mode')
            )
            return

        custom_apps = [
            'api'
        ]

        models_to_reset = []
        for app in custom_apps:
            models_to_reset.extend(
                apps.get_app_config(app).get_models()
            )

        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                cursor.execute('SET session_replication_role = replica;')

            try:
                for model in models_to_reset:
                    table_name = model._meta.db_table
                    self.stdout.write(f"Resetting table: {table_name}")

                    cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")

                cursor.execute("Set session_replication_role = DEFAULT;")
                self.stdout.write(self.style.SUCCESS('Database tables and sequences reset successfully'))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error resetting database tables and sequences: {str(e)}')
                )
                raise