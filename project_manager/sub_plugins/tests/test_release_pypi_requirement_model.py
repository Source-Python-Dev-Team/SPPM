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
from project_manager.sub_plugins.models import (
    SubPluginRelease,
    SubPluginReleasePyPiRequirement,
)
from requirements.models import PyPiRequirement
from test_utils.factories.requirements import PyPiRequirementFactory
from test_utils.factories.sub_plugins import SubPluginReleasePyPiRequirementFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginReleasePyPiRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleasePyPiRequirement,
                AbstractUUIDPrimaryKeyModel,
            )
        )

    def test_sub_plugin_release_field(self):
        field = SubPluginReleasePyPiRequirement._meta.get_field('sub_plugin_release')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=SubPluginRelease,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_pypi_requirement_field(self):
        field = SubPluginReleasePyPiRequirement._meta.get_field(
            'pypi_requirement',
        )
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=PyPiRequirement,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_version_field(self):
        field = SubPluginReleasePyPiRequirement._meta.get_field('version')
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
                'The version of the PyPi package for this release of the '
                'sub_plugin.'
            )
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_optional_field(self):
        field = SubPluginReleasePyPiRequirement._meta.get_field('optional')
        self.assertIsInstance(
            obj=field,
            cls=models.BooleanField,
        )
        self.assertFalse(expr=field.default)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        requirement = PyPiRequirementFactory()
        version = '.'.join(map(str, sample(range(100), 3)))
        self.assertEqual(
            first=str(
                SubPluginReleasePyPiRequirementFactory(
                    pypi_requirement=requirement,
                    version=version,
                )
            ),
            second=f'{requirement.name} - {version}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=SubPluginReleasePyPiRequirement._meta.unique_together,
            tuple2=(('sub_plugin_release', 'pypi_requirement'),),
        )
        self.assertEqual(
            first=SubPluginReleasePyPiRequirement._meta.verbose_name,
            second='SubPlugin Release PyPi Requirement',
        )
        self.assertEqual(
            first=SubPluginReleasePyPiRequirement._meta.verbose_name_plural,
            second='SubPlugin Release PyPi Requirements',
        )
