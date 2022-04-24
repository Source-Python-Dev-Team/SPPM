# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# App
from project_manager.api.common.filtersets import ProjectFilterSet
from project_manager.sub_plugins.api.filtersets import SubPluginFilterSet
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# TEST CASES
# =============================================================================
class PackageFilterSetTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginFilterSet, ProjectFilterSet))

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginFilterSet.Meta,
                ProjectFilterSet.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginFilterSet.Meta.model,
            second=SubPlugin,
        )
