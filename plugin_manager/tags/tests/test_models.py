# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import IntegrityError
from django.test import TestCase

# App
from ..models import Tag


# =============================================================================
# >> TEST CLASSES
# =============================================================================
class TestTag(TestCase):
    def test_name_must_be_unique(self):
        Tag.objects.create(name='test')
        self.assertRaises(
            IntegrityError,
            Tag.objects.create,
            name='test',
        )
