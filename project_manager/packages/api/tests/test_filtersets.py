# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# App
from project_manager.common.api.filtersets import ProjectFilterSet
from project_manager.packages.api.filtersets import PackageFilterSet
from project_manager.packages.models import Package


# =============================================================================
# TEST CASES
# =============================================================================
class PackageFilterSetTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(PackageFilterSet, ProjectFilterSet))

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageFilterSet.Meta,
                ProjectFilterSet.Meta,
            ),
        )
        self.assertEqual(
            first=PackageFilterSet.Meta.model,
            second=Package,
        )
