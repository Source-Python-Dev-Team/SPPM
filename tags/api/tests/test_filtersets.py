# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from django_filters.filterset import FilterSet

# App
from tags.api.filtersets import TagFilterSet
from tags.models import Tag


# =============================================================================
# TEST CASES
# =============================================================================
class TagFilterSetTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(TagFilterSet, FilterSet),
        )

    def test_meta_class(self):
        self.assertEqual(
            first=TagFilterSet.Meta.model,
            second=Tag,
        )
        self.assertTupleEqual(
            tuple1=TagFilterSet.Meta.fields,
            tuple2=('black_listed',),
        )
