# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.packages.models import (
    Package,
    PackageTag,
)
from tags.models import Tag
from test_utils.factories.packages import PackageTagFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PackageTagTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageTag, AbstractUUIDPrimaryKeyModel)
        )

    def test_package_field(self):
        field = PackageTag._meta.get_field('package')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Package,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_tag_field(self):
        field = PackageTag._meta.get_field('tag')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Tag,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = PackageTagFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.package} Tag: {obj.tag}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PackageTag._meta.unique_together,
            tuple2=(('package', 'tag'),),
        )
        self.assertEqual(
            first=PackageTag._meta.verbose_name,
            second='Package Tag',
        )
        self.assertEqual(
            first=PackageTag._meta.verbose_name_plural,
            second='Package Tags',
        )
