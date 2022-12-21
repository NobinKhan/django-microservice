"""
Django command to wait for the database to be available.
"""
import time
from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                time.sleep(2)
                self.check(databases=settings.DATABASES)
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 3 second...')
                time.sleep(3)
            except Exception as msg:
                self.stdout.write(msg.args[0])
            else:
                db_up = True

        self.stdout.write(self.style.SUCCESS('Database available!'))


# if __name__== "__main__":
#     hd = Command()
#     hd.handle()