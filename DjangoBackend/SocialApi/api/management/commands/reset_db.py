from django.core.management import BaseCommand, call_command
from django.db import connection
from django.apps import apps
from django.conf import settings
from django.db.migrations.loader import MigrationLoader


class Command(BaseCommand):
    help = 'Reset Database tables and sequences for the api testing'

    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            self.stdout.write(
                self.style.ERROR('This command can only be run in DEBUG mode')
            )
            return

        with connection.cursor() as cursor:
            self.stdout.write('Dropping token blacklist tables...')
            cursor.execute("""
                DROP TABLE IF EXISTS token_blacklist_outstandingtoken CASCADE;
                DROP TABLE IF EXISTS token_blacklist_blacklistedtoken CASCADE;
                DELETE FROM django_migrations WHERE app = 'token_blacklist';
            """)


        custom_apps = [
            'api'
        ]

        try:
            self.stdout.write('Checking for pending migrations...')
            call_command('makemigrations', '--check', '--dry-run')

            # get a list of apps that have migrations
            loader = MigrationLoader(connection)
            apps_with_migrations = {migration[0] for migration in loader.applied_migrations}


            #Revert custom apps migrations if migrations exist
            for app in custom_apps:
                if app in apps_with_migrations:
                    self.stdout.write(f"Reverting Migrations for {app}")
                    call_command('migrate', app, 'zero')

            django_apps = [
                'admin',
                'sessions',
                'rest_framework_simplejwt.token_blacklist',
                'auth',
                'contenttypes'
            ]
            #Revert migrations for a builtin app if they exist

            for app in django_apps:
                if app in apps_with_migrations:
                    self.stdout.write(f"Reverting Migrations for {app}")
                    call_command("migrate", app, "zero")

            self.stdout.write('Resetting database...')
            call_command('migrate')

            self.stdout.write(self.style.SUCCESS('Database reset successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
            raise