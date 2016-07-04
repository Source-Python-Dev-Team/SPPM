# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import IntegrityError
from django.test import TestCase

# App
from ..models import SubPluginPath


# =============================================================================
# >> TESTS
# =============================================================================
class TestSubPluginPath(TestCase):
    def test_plugin_is_required(self):
        self.assertRaisesMessage(
            IntegrityError,
            (
                'NOT NULL constraint failed: '
                'plugin_manager_subpluginpath.plugin_id'
            ),
            SubPluginPath.objects.create,
        )
