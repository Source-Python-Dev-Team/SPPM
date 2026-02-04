# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import ProjectImage
from project_manager.packages.models import (
    Package,
    PackageImage,
)
from test_utils.factories.packages import PackageImageFactory
from test_utils.helpers import get_new_fields_for_model


# =============================================================================
# TEST CASES
# =============================================================================
class PackageImageTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTupleEqual(
            tuple1=PackageImage.__bases__,
            tuple2=(ProjectImage,),
        )

    def test_field_names(self):
        self.assertSetEqual(
            set1=get_new_fields_for_model(PackageImage),
            set2={
                "package",
            },
        )

    def test_package_field(self):
        field = PackageImage._meta.get_field("package")
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
        self.assertEqual(
            first=getattr(field.remote_field, "related_name"),
            second="images",
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = PackageImageFactory()
        self.assertEqual(
            first=str(obj),
            second=f"{obj.package} - {obj.image}",
        )

    def test_meta_class(self):
        self.assertEqual(
            first=PackageImage._meta.verbose_name,
            second="Package Image",
        )
        self.assertEqual(
            first=PackageImage._meta.verbose_name_plural,
            second="Package Images",
        )
