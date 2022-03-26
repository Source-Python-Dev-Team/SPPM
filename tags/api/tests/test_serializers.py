# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from rest_framework.fields import IntegerField
from rest_framework.relations import ManyRelatedField, RelatedField
from rest_framework.serializers import ModelSerializer

# App
from tags.api.serializers import (
    RelatedTagSerializer,
    TagListSerializer,
    TagRetrieveSerializer,
)
from tags.models import Tag


# =============================================================================
# TEST CASES
# =============================================================================
class RelatedTagSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(RelatedTagSerializer, RelatedField))


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

        for field in (
            'packages',
            'plugins',
            'subplugins',
        ):
            self.assertIn(
                member=field,
                container=declared_fields,
            )
            obj = declared_fields[field]
            self.assertIsInstance(
                obj=obj,
                cls=ManyRelatedField,
            )
            self.assertIsInstance(
                obj=obj.child_relation,
                cls=RelatedTagSerializer,
            )
            self.assertTrue(expr=obj.child_relation.read_only)

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
