# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet

# App
from project_manager.api.common.filtersets import ProjectFilterSet


# =============================================================================
# TEST CASES
# =============================================================================
class ProjectFilterSetTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectFilterSet, FilterSet),
        )

    def test_base_filters(self):
        base_filters = ProjectFilterSet.base_filters
        self.assertEqual(
            first=len(base_filters),
            second=3,
        )

        self.assertIn(
            member='game',
            container=base_filters,
        )
        self.assertIsInstance(
            obj=base_filters['game'],
            cls=CharFilter,
        )
        self.assertEqual(
            first=base_filters['game'].field_name,
            second='supported_games__basename',
        )
        self.assertEqual(
            first=base_filters['game'].label,
            second='Game',
        )

        self.assertIn(
            member='tag',
            container=base_filters,
        )
        self.assertIsInstance(
            obj=base_filters['tag'],
            cls=CharFilter,
        )
        self.assertEqual(
            first=base_filters['tag'].field_name,
            second='tags__name',
        )
        self.assertEqual(
            first=base_filters['tag'].label,
            second='Tag',
        )

        self.assertIn(
            member='user',
            container=base_filters,
        )
        self.assertIsInstance(
            obj=base_filters['user'],
            cls=CharFilter,
        )
        self.assertEqual(
            first=base_filters['user'].method,
            second='filter_user',
        )
        self.assertEqual(
            first=base_filters['user'].label,
            second='User',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ProjectFilterSet.Meta.fields,
            tuple2=(
                'game',
                'tag',
                'user',
            ),
        )
