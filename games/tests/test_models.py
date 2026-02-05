# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# Third Party Django
from rest_framework.reverse import reverse

# App
from games.constants import (
    GAME_BASENAME_MAX_LENGTH,
    GAME_NAME_MAX_LENGTH,
    GAME_SLUG_MAX_LENGTH,
)
from games.management.commands.create_game_instances import GAMES
from games.models import Game
from test_utils.factories.games import GameFactory
from test_utils.helpers import get_new_fields_for_model


# =============================================================================
# TEST CASES
# =============================================================================
class GameTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTupleEqual(
            tuple1=Game.__bases__,
            tuple2=(models.Model,),
        )

    def test_field_names(self):
        self.assertSetEqual(
            set1=get_new_fields_for_model(Game),
            set2={
                "name",
                "basename",
                "slug",
                "icon",
            },
        )

    def test_name_field(self):
        field = Game._meta.get_field("name")
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
        field = Game._meta.get_field("basename")
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
        field = Game._meta.get_field("slug")
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
        field = Game._meta.get_field("icon")
        self.assertIsInstance(
            obj=field,
            cls=models.ImageField,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertEqual(
            first=Game._meta.verbose_name,
            second="Game",
        )
        self.assertEqual(
            first=Game._meta.verbose_name_plural,
            second="Games",
        )

    def test__str__(self):
        game = list(GAMES)[0]
        obj = GameFactory(
            name=GAMES[game],
            basename=game,
            icon=f"games/{game}.png",
        )
        self.assertEqual(
            first=str(obj),
            second=obj.name,
        )

    def test_get_absolute_url(self):
        game = GameFactory()
        self.assertEqual(
            first=game.get_absolute_url(),
            second=reverse(
                viewname="games:detail",
                kwargs={
                    "pk": game.pk,
                },
            ),
        )
