# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from rest_framework.fields import IntegerField
from rest_framework.serializers import ListSerializer, ModelSerializer

# App
from project_manager.packages.api.common.serializers import MinimalPackageSerializer
from project_manager.plugins.api.common.serializers import MinimalPluginSerializer
from project_manager.sub_plugins.api.common.serializers import MinimalSubPluginSerializer
from tags.api.serializers import TagListSerializer, TagRetrieveSerializer
from tags.models import Tag


# =============================================================================
# TEST CASES
# =============================================================================
class TagRetrieveSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(TagRetrieveSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(TagRetrieveSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=3,
        )

        for field, cls in (
            ('packages', MinimalPackageSerializer),
            ('plugins', MinimalPluginSerializer),
            ('subplugins', MinimalSubPluginSerializer),
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
            first=TagRetrieveSerializer.Meta.model,
            second=Tag,
        )
        self.assertTupleEqual(
            tuple1=TagRetrieveSerializer.Meta.fields,
            tuple2=(
                'name',
                'packages',
                'plugins',
                'subplugins',
            ),
        )


class TagListSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(TagListSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(TagListSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=4,
        )

        for field in (
            'package_count',
            'plugin_count',
            'subplugin_count',
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
            first=TagListSerializer.Meta.model,
            second=Tag,
        )
        self.assertTupleEqual(
            tuple1=TagListSerializer.Meta.fields,
            tuple2=(
                'name',
                'package_count',
                'plugin_count',
                'subplugin_count',
                'project_count',
            ),
        )
