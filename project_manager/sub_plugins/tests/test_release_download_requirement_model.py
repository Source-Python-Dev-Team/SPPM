# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.test import TestCase

# App
from project_manager.models.abstract import AbstractUUIDPrimaryKeyModel
from project_manager.sub_plugins.models import (
    SubPluginRelease,
    SubPluginReleaseDownloadRequirement,
)
from requirements.models import DownloadRequirement
from test_utils.factories.requirements import DownloadRequirementFactory
from test_utils.factories.sub_plugins import SubPluginReleaseDownloadRequirementFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginReleaseDownloadRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleaseDownloadRequirement,
                AbstractUUIDPrimaryKeyModel,
            )
        )

    def test_sub_plugin_release_field(self):
        field = SubPluginReleaseDownloadRequirement._meta.get_field('sub_plugin_release')
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

    def test_download_requirement_field(self):
        field = SubPluginReleaseDownloadRequirement._meta.get_field(
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
        field = SubPluginReleaseDownloadRequirement._meta.get_field('optional')
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
                SubPluginReleaseDownloadRequirementFactory(
                    download_requirement=requirement,
                )
            ),
            second=requirement.url,
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=SubPluginReleaseDownloadRequirement._meta.unique_together,
            tuple2=(('sub_plugin_release', 'download_requirement'),),
        )
        self.assertEqual(
            first=SubPluginReleaseDownloadRequirement._meta.verbose_name,
            second='SubPlugin Release Download Requirement',
        )
        self.assertEqual(
            first=SubPluginReleaseDownloadRequirement._meta.verbose_name_plural,
            second='SubPlugin Release Download Requirements',
        )
