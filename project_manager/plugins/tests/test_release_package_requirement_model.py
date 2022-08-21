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
from project_manager.packages.models import Package
from project_manager.plugins.models import (
    PluginRelease,
    PluginReleasePackageRequirement,
)
from test_utils.factories.packages import PackageFactory
from test_utils.factories.plugins import PluginReleasePackageRequirementFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PluginReleasePackageRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleasePackageRequirement,
                AbstractUUIDPrimaryKeyModel,
            )
        )

    def test_plugin_release_field(self):
        field = PluginReleasePackageRequirement._meta.get_field('plugin_release')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=PluginRelease,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_package_requirement_field(self):
        field = PluginReleasePackageRequirement._meta.get_field(
            'package_requirement',
        )
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

    def test_version_field(self):
        field = PluginReleasePackageRequirement._meta.get_field('version')
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
                'The version of the custom package for this release of the '
                'plugin.'
            )
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_optional_field(self):
        field = PluginReleasePackageRequirement._meta.get_field('optional')
        self.assertIsInstance(
            obj=field,
            cls=models.BooleanField,
        )
        self.assertFalse(expr=field.default)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        requirement = PackageFactory()
        version = '.'.join(map(str, sample(range(100), 3)))
        self.assertEqual(
            first=str(
                PluginReleasePackageRequirementFactory(
                    package_requirement=requirement,
                    version=version,
                )
            ),
            second=f'{requirement.name} - {version}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PluginReleasePackageRequirement._meta.unique_together,
            tuple2=(('plugin_release', 'package_requirement'),),
        )
        self.assertEqual(
            first=PluginReleasePackageRequirement._meta.verbose_name,
            second='Plugin Release Package Requirement',
        )
        self.assertEqual(
            first=PluginReleasePackageRequirement._meta.verbose_name_plural,
            second='Plugin Release Package Requirements',
        )
