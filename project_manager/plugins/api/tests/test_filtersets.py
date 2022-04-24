# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# App
from project_manager.api.common.filtersets import ProjectFilterSet
from project_manager.plugins.api.filtersets import PluginFilterSet
from project_manager.plugins.models import Plugin


# =============================================================================
# TEST CASES
# =============================================================================
class PluginFilterSetTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(PluginFilterSet, ProjectFilterSet))

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginFilterSet.Meta,
                ProjectFilterSet.Meta,
            ),
        )
        self.assertEqual(
            first=PluginFilterSet.Meta.model,
            second=Plugin,
        )
