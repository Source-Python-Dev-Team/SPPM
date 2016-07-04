# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import IntegrityError
from django.test import TestCase

# App
from ..models import Game


# =============================================================================
# >> TESTS
# =============================================================================
class TestGame(TestCase):
    def test_name_must_be_unique(self):
        Game.objects.create(name='Test', basename='test')
        self.assertRaises(
            IntegrityError,
            Game.objects.create,
            name='Test',
            basename='test2',
        )

    def test_basename_must_be_unique(self):
        Game.objects.create(name='Test', basename='test')
        self.assertRaises(
            IntegrityError,
            Game.objects.create,
            name='Test2',
            basename='test',
        )

    def test_slug_must_be_unique(self):
        Game.objects.create(name='Test', basename='test')
        self.assertRaises(
            IntegrityError,
            Game.objects.create,
            name='Test2',
            basename='TEST',
        )
