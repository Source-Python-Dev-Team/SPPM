# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

# App
from requirements.api.serializers.common import (
    ReleaseDownloadRequirementSerializer,
    ReleasePyPiRequirementSerializer,
    ReleaseVersionControlRequirementSerializer,
)


# =============================================================================
# TEST CASES
# =============================================================================
class ReleaseDownloadRequirementSerializerTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ReleaseDownloadRequirementSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ReleaseDownloadRequirementSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=1,
        )

        self.assertIn(
            member='url',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['url'],
            cls=ReadOnlyField,
        )
        self.assertEqual(
            first=declared_fields['url'].source,
            second='download_requirement.url',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ReleaseDownloadRequirementSerializer.Meta.fields,
            tuple2=(
                'url',
                'optional',
            ),
        )


class ReleasePyPiRequirementSerializerTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ReleasePyPiRequirementSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ReleasePyPiRequirementSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=3,
        )

        self.assertIn(
            member='name',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['name'],
            cls=ReadOnlyField,
        )
        self.assertEqual(
            first=declared_fields['name'].source,
            second='pypi_requirement.name',
        )

        self.assertIn(
            member='slug',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['slug'],
            cls=ReadOnlyField,
        )
        self.assertEqual(
            first=declared_fields['slug'].source,
            second='pypi_requirement.slug',
        )

        self.assertIn(
            member='version',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['version'],
            cls=ReadOnlyField,
        )
        self.assertIsNone(obj=declared_fields['version'].source)

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ReleasePyPiRequirementSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
                'version',
                'optional',
            ),
        )


class ReleaseVersionControlRequirementSerializerTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ReleaseVersionControlRequirementSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ReleaseVersionControlRequirementSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=2,
        )

        self.assertIn(
            member='url',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['url'],
            cls=ReadOnlyField,
        )
        self.assertEqual(
            first=declared_fields['url'].source,
            second='vcs_requirement.url',
        )

        self.assertIn(
            member='version',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['version'],
            cls=ReadOnlyField,
        )
        self.assertIsNone(obj=declared_fields['version'].source)

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ReleaseVersionControlRequirementSerializer.Meta.fields,
            tuple2=(
                'url',
                'version',
                'optional',
            ),
        )
