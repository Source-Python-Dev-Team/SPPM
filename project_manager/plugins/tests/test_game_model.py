# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from games.models import Game
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.plugins.models import (
    Plugin,
    PluginGame,
)
from test_utils.factories.plugins import PluginGameFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PluginGameTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginGame, AbstractUUIDPrimaryKeyModel)
        )

    def test_plugin_field(self):
        field = PluginGame._meta.get_field('plugin')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Plugin,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_game_field(self):
        field = PluginGame._meta.get_field('game')
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
        obj = PluginGameFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.plugin} Game: {obj.game}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PluginGame._meta.unique_together,
            tuple2=(('plugin', 'game'),),
        )
        self.assertEqual(
            first=PluginGame._meta.verbose_name,
            second='Plugin Game',
        )
        self.assertEqual(
            first=PluginGame._meta.verbose_name_plural,
            second='Plugin Games',
        )
