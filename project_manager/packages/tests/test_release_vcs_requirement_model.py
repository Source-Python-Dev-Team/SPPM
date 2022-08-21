# =============================================================================
# IMPORTS
# =============================================================================
# Python
from random import sample

# Django
from django.db import models
from django.test import TestCase

# App
from project_manager.constants import RELEASE_VERSION_MAX_LENGTH
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.validators import version_validator
from project_manager.packages.models import (
    PackageRelease,
    PackageReleaseVersionControlRequirement,
)
from requirements.models import VersionControlRequirement
from test_utils.factories.packages import PackageReleaseVersionControlRequirementFactory
from test_utils.factories.requirements import VersionControlRequirementFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PackageReleaseVersionControlRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleaseVersionControlRequirement,
                AbstractUUIDPrimaryKeyModel,
            )
        )

    def test_package_release_field(self):
        field = PackageReleaseVersionControlRequirement._meta.get_field('package_release')
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

    def test_vcs_requirement_field(self):
        field = PackageReleaseVersionControlRequirement._meta.get_field(
            'vcs_requirement',
        )
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=VersionControlRequirement,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_version_field(self):
        field = PackageReleaseVersionControlRequirement._meta.get_field(
            'version',
        )
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=RELEASE_VERSION_MAX_LENGTH,
        )
        self.assertIn(
            member=version_validator,
            container=field.validators,
        )
        self.assertEqual(
            first=field.help_text,
            second=(
                'The version of the VCS package for this release of the '
                'package.'
            )
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_optional_field(self):
        field = PackageReleaseVersionControlRequirement._meta.get_field(
            'optional',
        )
        self.assertIsInstance(
            obj=field,
            cls=models.BooleanField,
        )
        self.assertFalse(expr=field.default)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        requirement = VersionControlRequirementFactory()
        version = '.'.join(map(str, sample(range(100), 3)))
        self.assertEqual(
            first=str(
                PackageReleaseVersionControlRequirementFactory(
                    vcs_requirement=requirement,
                    version=version,
                )
            ),
            second=f'{requirement.url} - {version}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PackageReleaseVersionControlRequirement._meta.unique_together,
            tuple2=(('package_release', 'vcs_requirement'),),
        )
        self.assertEqual(
            first=PackageReleaseVersionControlRequirement._meta.verbose_name,
            second='Package Release Version Control Requirement',
        )
        self.assertEqual(
            first=PackageReleaseVersionControlRequirement._meta.verbose_name_plural,
            second='Package Release Version Control Requirements',
        )
