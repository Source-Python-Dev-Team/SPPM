# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.plugins.models import (
    PluginRelease,
    PluginReleaseDownloadRequirement,
)
from requirements.models import DownloadRequirement
from test_utils.factories.plugins import PluginReleaseDownloadRequirementFactory
from test_utils.factories.requirements import DownloadRequirementFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PluginReleaseDownloadRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleaseDownloadRequirement,
                AbstractUUIDPrimaryKeyModel,
            )
        )

    def test_plugin_release_field(self):
        field = PluginReleaseDownloadRequirement._meta.get_field('plugin_release')
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

    def test_download_requirement_field(self):
        field = PluginReleaseDownloadRequirement._meta.get_field(
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
        field = PluginReleaseDownloadRequirement._meta.get_field('optional')
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
                PluginReleaseDownloadRequirementFactory(
                    download_requirement=requirement,
                )
            ),
            second=requirement.url,
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PluginReleaseDownloadRequirement._meta.unique_together,
            tuple2=(('plugin_release', 'download_requirement'),),
        )
        self.assertEqual(
            first=PluginReleaseDownloadRequirement._meta.verbose_name,
            second='Plugin Release Download Requirement',
        )
        self.assertEqual(
            first=PluginReleaseDownloadRequirement._meta.verbose_name_plural,
            second='Plugin Release Download Requirements',
        )
