"""
Test custom Django management commands.
"""
from unittest.mock import patch  # to mock behaviour of database
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# @patch('core.management.commands.wait_for_db.Command.check')
# django.db.utils.ConnectionHandler
# core.management.commands.wait_for_db.Command.check


@patch('django.db.utils.ConnectionHandler.__getitem__')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True
        call_command('wait_for_db')
        print(patched_check.call_count)
        self.assertEqual(patched_check.call_count, 1)

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        # patches(decorators) are clled from inside out
        """Test waiting for database when getting OperationalError"""
        # Add a side effect to mock object as raise Psycopg2Error
        # error 2 times and OprationalError 3 times then True
        # Psycopg2Error is thrown when postgres has not
        # even stated yet
        # OperationalError is thrown when database is
        # not setup yet after postgre has started
        patched_check.side_effect = [Psycopg2Error] * 2 \
            + [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
