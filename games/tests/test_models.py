from django.db import models
from django.test import TestCase

from games.constants import (
    GAME_BASENAME_MAX_LENGTH,
    GAME_NAME_MAX_LENGTH,
    GAME_SLUG_MAX_LENGTH,
)
from games.models import Game


class GameTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(Game, models.Model),
        )

    def test_name_field(self):
        field = Game._meta.get_field('name')
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=GAME_NAME_MAX_LENGTH,
        )
        self.assertTrue(expr=field.unique)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_basename_field(self):
        field = Game._meta.get_field('basename')
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=GAME_BASENAME_MAX_LENGTH,
        )
        self.assertTrue(expr=field.unique)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_slug_field(self):
        field = Game._meta.get_field('slug')
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=GAME_SLUG_MAX_LENGTH,
        )
        self.assertTrue(expr=field.unique)
        self.assertTrue(expr=field.primary_key)
        self.assertTrue(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_icon_field(self):
        field = Game._meta.get_field('icon')
        self.assertIsInstance(
            obj=field,
            cls=models.ImageField,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)
