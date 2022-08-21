# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.packages.models import (
    PackageRelease,
    PackageReleaseDownloadRequirement,
)
from requirements.models import DownloadRequirement
from test_utils.factories.packages import PackageReleaseDownloadRequirementFactory
from test_utils.factories.requirements import DownloadRequirementFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PackageReleaseDownloadRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleaseDownloadRequirement,
                AbstractUUIDPrimaryKeyModel,
            )
        )

    def test_package_release_field(self):
        field = PackageReleaseDownloadRequirement._meta.get_field('package_release')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=PackageRelease,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_download_requirement_field(self):
        field = PackageReleaseDownloadRequirement._meta.get_field(
            'download_requirement',
        )
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=DownloadRequirement,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_optional_field(self):
        field = PackageReleaseDownloadRequirement._meta.get_field('optional')
        self.assertIsInstance(
            obj=field,
            cls=models.BooleanField,
        )
        self.assertFalse(expr=field.default)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        requirement = DownloadRequirementFactory()
        self.assertEqual(
            first=str(
                PackageReleaseDownloadRequirementFactory(
                    download_requirement=requirement,
                )
            ),
            second=requirement.url,
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PackageReleaseDownloadRequirement._meta.unique_together,
            tuple2=(('package_release', 'download_requirement'),),
        )
        self.assertEqual(
            first=PackageReleaseDownloadRequirement._meta.verbose_name,
            second='Package Release Download Requirement',
        )
        self.assertEqual(
            first=PackageReleaseDownloadRequirement._meta.verbose_name_plural,
            second='Package Release Download Requirements',
        )
