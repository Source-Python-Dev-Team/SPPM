# =============================================================================
# IMPORTS
# =============================================================================
# Python
import sys
from io import StringIO

# Django
from django.core.management import call_command
from django.test import TestCase


# =============================================================================
# TEST CASES
# =============================================================================
class MigrationTest(TestCase):

    def test_pending_migrations(self):
        out, sys.stdout = sys.stdout, StringIO()
        call_command('makemigrations', '--dry-run')
        sys.stdout.seek(0)
        output = sys.stdout.read()
        sys.stdout = out
        self.assertEqual(
            first=output,
            second='No changes detected\n',
        )
