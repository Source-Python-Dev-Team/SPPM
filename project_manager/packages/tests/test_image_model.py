# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# Third Party Django
from model_utils.fields import AutoCreatedField

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.packages.helpers import handle_package_image_upload
from project_manager.packages.models import (
    Package,
    PackageImage,
)
from test_utils.factories.packages import PackageImageFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PackageImageTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageImage, AbstractUUIDPrimaryKeyModel)
        )

    def test_package_field(self):
        field = PackageImage._meta.get_field('package')
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
        self.assertEqual(
            first=field.remote_field.related_name,
            second='images',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_image_field(self):
        field = PackageImage._meta.get_field('image')
        self.assertIsInstance(
            obj=field,
            cls=models.ImageField,
        )
        self.assertEqual(
            first=field.upload_to,
            second=handle_package_image_upload,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_created_field(self):
        field = PackageImage._meta.get_field('created')
        self.assertIsInstance(
            obj=field,
            cls=AutoCreatedField,
        )
        self.assertEqual(
            first=field.verbose_name,
            second='created',
        )

    def test__str__(self):
        obj = PackageImageFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.package} - {obj.image}',
        )

    def test_meta_class(self):
        self.assertEqual(
            first=PackageImage._meta.verbose_name,
            second='Package Image',
        )
        self.assertEqual(
            first=PackageImage._meta.verbose_name_plural,
            second='Package Images',
        )
