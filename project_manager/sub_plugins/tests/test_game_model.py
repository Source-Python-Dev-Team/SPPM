# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from games.models import Game
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginGame,
)
from test_utils.factories.sub_plugins import SubPluginGameFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginGameTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginGame, AbstractUUIDPrimaryKeyModel)
        )

    def test_sub_plugin_field(self):
        field = SubPluginGame._meta.get_field('sub_plugin')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=SubPlugin,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_game_field(self):
        field = SubPluginGame._meta.get_field('game')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Game,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = SubPluginGameFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.sub_plugin} Game: {obj.game}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=SubPluginGame._meta.unique_together,
            tuple2=(('sub_plugin', 'game'),),
        )
        self.assertEqual(
            first=SubPluginGame._meta.verbose_name,
            second='SubPlugin Game',
        )
        self.assertEqual(
            first=SubPluginGame._meta.verbose_name_plural,
            second='SubPlugin Games',
        )
