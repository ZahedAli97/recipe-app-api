"""
Django command to wait for database to be available
"""
import time

from django.db import connections

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

# Psycopg2Error is thrown when postgres has not even stated yet
# OperationalError is thrown when database is not
# setup yet after postgre has started


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('\nWaiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
