# =============================================================================
# IMPORTS
# =============================================================================
# Python
from io import StringIO

# Django
from django.core.management import call_command
from django.test import TestCase


# =============================================================================
# TEST CASES
# =============================================================================
class MigrationTest(TestCase):

    def test_pending_migrations(self):
        output = StringIO()
        call_command("makemigrations", "--dry-run", stdout=output)
        self.assertEqual(
            first=output.getvalue(),
            second="No changes detected\n",
        )
