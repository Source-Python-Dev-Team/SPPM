# =============================================================================
# IMPORTS
# =============================================================================
# Python
from datetime import timedelta

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

# Third Party Django
from model_utils.tracker import FieldTracker

# App
from project_manager.models.abstract import ProjectRelease
from project_manager.packages.models import Package
from project_manager.plugins.helpers import handle_plugin_zip_upload
from project_manager.plugins.models import (
    Plugin,
    PluginRelease,
    PluginReleaseDownloadRequirement,
    PluginReleasePackageRequirement,
    PluginReleasePyPiRequirement,
    PluginReleaseVersionControlRequirement,
)
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from test_utils.factories.plugins import (
    PluginFactory,
    PluginReleaseFactory,
)
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class PluginReleaseTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginRelease, ProjectRelease)
        )

    def test_plugin_field(self):
        field = PluginRelease._meta.get_field('plugin')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Plugin,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='releases',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_created_by_field(self):
        field = PluginRelease._meta.get_field('created_by')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=ForumUser,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.SET_NULL,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='plugin_releases',
        )
        self.assertFalse(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_download_requirements_field(self):
        field = PluginRelease._meta.get_field('download_requirements')
        self.assertIsInstance(
            obj=field,
            cls=models.ManyToManyField,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=DownloadRequirement,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='required_in_plugin_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PluginReleaseDownloadRequirement,
        )

    def test_package_requirements_field(self):
        field = PluginRelease._meta.get_field('package_requirements')
        self.assertIsInstance(
            obj=field,
            cls=models.ManyToManyField,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Package,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='required_in_plugin_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PluginReleasePackageRequirement,
        )

    def test_pypi_requirements_field(self):
        field = PluginRelease._meta.get_field('pypi_requirements')
        self.assertIsInstance(
            obj=field,
            cls=models.ManyToManyField,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=PyPiRequirement,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='required_in_plugin_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PluginReleasePyPiRequirement,
        )

    def test_vcs_requirements_field(self):
        field = PluginRelease._meta.get_field('vcs_requirements')
        self.assertIsInstance(
            obj=field,
            cls=models.ManyToManyField,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=VersionControlRequirement,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='required_in_plugin_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PluginReleaseVersionControlRequirement,
        )

    def test_field_tracker(self):
        self.assertTrue(expr=hasattr(PluginRelease, 'field_tracker'))
        self.assertIsInstance(
            obj=PluginRelease.field_tracker,
            cls=FieldTracker,
        )
        self.assertSetEqual(
            set1=PluginRelease.field_tracker.fields,
            set2={'version'},
        )

    def test_primary_attributes(self):
        self.assertEqual(
            first=PluginRelease.handle_zip_file_upload,
            second=handle_plugin_zip_upload,
        )
        self.assertEqual(
            first=PluginRelease.project_class,
            second=Plugin,
        )

    def test_file_name(self):
        file_name = 'test.zip'
        release = PluginReleaseFactory(
            zip_file=f'directory/path/{file_name}',
        )
        self.assertEqual(
            first=release.file_name,
            second=file_name,
        )

    def test__str__(self):
        release = PluginReleaseFactory()
        self.assertEqual(
            first=str(release),
            second=f'{release.plugin} - {release.version}',
        )

    def test_clean(self):
        release = PluginReleaseFactory(
            version='1.0.0',
        )
        PluginReleaseFactory(
            plugin=release.plugin,
            version='1.0.1',
        )

        release.clean()
        release.version = '1.0.2'
        release.clean()

        release.version = '1.0.1'
        with self.assertRaises(ValidationError) as context:
            release.clean()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={'version': ['Version already exists.']}
        )

    def test_save(self):
        original_updated = now()
        plugin = PluginFactory(
            created=original_updated,
            updated=original_updated,
        )
        release_created = original_updated + timedelta(minutes=1)
        PluginReleaseFactory(
            pk=None,
            plugin=plugin,
            created=release_created,
            version='1.0.0',
        )
        self.assertEqual(
            first=Plugin.objects.get(pk=plugin.pk).updated,
            second=release_created,
        )

    def test_get_absolute_url(self):
        release = PluginReleaseFactory(zip_file='/test/this.py')
        self.assertEqual(
            first=release.get_absolute_url(),
            second=reverse(
                viewname='plugin-download',
                kwargs={
                    'slug': release.plugin.slug,
                    'zip_file': release.file_name,
                },
            ),
        )

    def test_meta_class(self):
        self.assertTrue(issubclass(PluginRelease.Meta, ProjectRelease.Meta))
        self.assertTupleEqual(
            tuple1=PluginRelease._meta.unique_together,
            tuple2=(('plugin', 'version'),),
        )
        self.assertEqual(
            first=PluginRelease._meta.verbose_name,
            second='Plugin Release',
        )
        self.assertEqual(
            first=PluginRelease._meta.verbose_name_plural,
            second='Plugin Releases',
        )
