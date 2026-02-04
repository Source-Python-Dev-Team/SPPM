# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from games.models import Game
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.packages.models import (
    Package,
    PackageGame,
)
from test_utils.factories.packages import PackageGameFactory
from test_utils.helpers import get_new_fields_for_model


# =============================================================================
# TEST CASES
# =============================================================================
class PackageGameTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTupleEqual(
            tuple1=PackageGame.__bases__,
            tuple2=(AbstractUUIDPrimaryKeyModel,),
        )

    def test_field_names(self):
        self.assertSetEqual(
            set1=get_new_fields_for_model(PackageGame),
            set2={
                "package",
                "game",
            },
        )

    def test_package_field(self):
        field = PackageGame._meta.get_field("package")
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Package,
        )
        self.assertEqual(
            first=getattr(field.remote_field, "on_delete"),
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_game_field(self):
        field = PackageGame._meta.get_field("game")
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Game,
        )
        self.assertEqual(
            first=getattr(field.remote_field, "on_delete"),
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = PackageGameFactory()
        self.assertEqual(
            first=str(obj),
            second=f"{obj.package} Game: {obj.game}",
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=getattr(PackageGame._meta, "unique_together"),
            tuple2=(("package", "game"),),
        )
        self.assertEqual(
            first=PackageGame._meta.verbose_name,
            second="Package Game",
        )
        self.assertEqual(
            first=PackageGame._meta.verbose_name_plural,
            second="Package Games",
        )
