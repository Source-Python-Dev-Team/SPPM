# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from django_filters.filters import BooleanFilter
from django_filters.filterset import FilterSet

# App
from users.api.filtersets import ForumUserFilterSet
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class ForumUserFilterSetTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ForumUserFilterSet, FilterSet),
        )

    def test_base_filters(self):
        base_filters = ForumUserFilterSet.base_filters
        self.assertEqual(
            first=len(base_filters),
            second=1,
        )

        self.assertIn(
            member='has_contributions',
            container=base_filters,
        )
        self.assertIsInstance(
            obj=base_filters['has_contributions'],
            cls=BooleanFilter,
        )
        self.assertEqual(
            first=base_filters['has_contributions'].method,
            second='filter_has_contributions',
        )
        self.assertEqual(
            first=base_filters['has_contributions'].label,
            second='Has Contributions',
        )

    def test_meta_class(self):
        self.assertEqual(
            first=ForumUserFilterSet.Meta.model,
            second=ForumUser,
        )
        self.assertTupleEqual(
            tuple1=ForumUserFilterSet.Meta.fields,
            tuple2=('has_contributions',),
        )
