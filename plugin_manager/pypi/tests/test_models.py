# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import IntegrityError
from django.test import TestCase

# App
from ..models import PyPiRequirement


# =============================================================================
# >> TEST CLASSES
# =============================================================================
class TestPyPiRequirement(TestCase):
    def test_name_must_be_unique(self):
        PyPiRequirement.objects.create(name='test')
        self.assertRaises(
            IntegrityError,
            PyPiRequirement.objects.create,
            name='test',
        )
