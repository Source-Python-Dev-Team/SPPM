# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from rest_framework.fields import IntegerField
from rest_framework.serializers import ListSerializer, ModelSerializer

# App
from games.api.common.serializers import MinimalGameSerializer
from games.api.serializers import GameListSerializer, GameRetrieveSerializer
from games.models import Game
from project_manager.packages.api.common.serializers import MinimalPackageSerializer
from project_manager.plugins.api.common.serializers import MinimalPluginSerializer
from project_manager.sub_plugins.api.common.serializers import MinimalSubPluginSerializer


# =============================================================================
# TEST CASES
# =============================================================================
class MinimalGameSerializerTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(MinimalGameSerializer, ModelSerializer),
        )

    def test_meta_class(self):
        self.assertEqual(
            first=MinimalGameSerializer.Meta.model,
            second=Game,
        )
        self.assertTupleEqual(
            tuple1=MinimalGameSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
                'icon',
            ),
        )


class GameRetrieveSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(GameRetrieveSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(GameRetrieveSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=3,
        )

        for field, cls in (
            ('packages', MinimalPackageSerializer),
            ('plugins', MinimalPluginSerializer),
            ('sub_plugins', MinimalSubPluginSerializer),
        ):
            self.assertIn(
                member=field,
                container=declared_fields,
            )
            obj = declared_fields[field]
            self.assertIsInstance(
                obj=obj,
                cls=ListSerializer,
            )
            self.assertTrue(expr=obj.read_only)
            self.assertIsInstance(
                obj=obj.child,
                cls=cls,
            )

    def test_meta_class(self):
        self.assertEqual(
            first=GameRetrieveSerializer.Meta.model,
            second=Game,
        )
        self.assertTupleEqual(
            tuple1=GameRetrieveSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
                'icon',
                'packages',
                'plugins',
                'sub_plugins',
            ),
        )


class GameListSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(GameListSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(GameListSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=4,
        )

        for field in (
            'package_count',
            'plugin_count',
            'sub_plugin_count',
            'project_count',
        ):
            self.assertIn(
                member=field,
                container=declared_fields,
            )
            obj = declared_fields[field]
            self.assertIsInstance(
                obj=obj,
                cls=IntegerField,
            )

    def test_meta_class(self):
        self.assertEqual(
            first=GameListSerializer.Meta.model,
            second=Game,
        )
        self.assertTupleEqual(
            tuple1=GameListSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
                'icon',
                'package_count',
                'plugin_count',
                'sub_plugin_count',
                'project_count',
            ),
        )
