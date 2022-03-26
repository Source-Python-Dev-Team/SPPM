# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from rest_framework.relations import ManyRelatedField, RelatedField
from rest_framework.serializers import ModelSerializer

# App
from tags.api.serializers import TagSerializer, RelatedTagSerializer
from tags.models import Tag
from users.api.serializers.common import ForumUserContributorSerializer


# =============================================================================
# TEST CASES
# =============================================================================
class RelatedTagSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(RelatedTagSerializer, RelatedField))


class TagSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(TagSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(TagSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=4,
        )

        self.assertIn(
            member='creator',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['creator'],
            cls=ForumUserContributorSerializer,
        )
        self.assertTrue(expr=declared_fields['creator'].read_only)

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
            first=TagSerializer.Meta.model,
            second=Tag,
        )
        self.assertTupleEqual(
            tuple1=TagSerializer.Meta.fields,
            tuple2=(
                'name',
                'packages',
                'plugins',
                'subplugins',
                'creator',
            ),
        )
