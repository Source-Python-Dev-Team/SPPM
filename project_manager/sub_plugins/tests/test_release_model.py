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
from project_manager.sub_plugins.helpers import handle_sub_plugin_zip_upload
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginRelease,
    SubPluginReleaseDownloadRequirement,
    SubPluginReleasePackageRequirement,
    SubPluginReleasePyPiRequirement,
    SubPluginReleaseVersionControlRequirement,
)
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from test_utils.factories.sub_plugins import (
    SubPluginFactory,
    SubPluginReleaseFactory,
)
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginReleaseTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginRelease, ProjectRelease)
        )

    def test_sub_plugin_field(self):
        field = SubPluginRelease._meta.get_field('sub_plugin')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=SubPlugin,
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
        field = SubPluginRelease._meta.get_field('created_by')
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
            second='sub_plugin_releases',
        )
        self.assertFalse(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_download_requirements_field(self):
        field = SubPluginRelease._meta.get_field('download_requirements')
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
            second='required_in_sub_plugin_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=SubPluginReleaseDownloadRequirement,
        )

    def test_package_requirements_field(self):
        field = SubPluginRelease._meta.get_field('package_requirements')
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
            second='required_in_sub_plugin_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=SubPluginReleasePackageRequirement,
        )

    def test_pypi_requirements_field(self):
        field = SubPluginRelease._meta.get_field('pypi_requirements')
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
            second='required_in_sub_plugin_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=SubPluginReleasePyPiRequirement,
        )

    def test_vcs_requirements_field(self):
        field = SubPluginRelease._meta.get_field('vcs_requirements')
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
            second='required_in_sub_plugin_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=SubPluginReleaseVersionControlRequirement,
        )

    def test_field_tracker(self):
        self.assertTrue(expr=hasattr(SubPluginRelease, 'field_tracker'))
        self.assertIsInstance(
            obj=SubPluginRelease.field_tracker,
            cls=FieldTracker,
        )
        self.assertSetEqual(
            set1=SubPluginRelease.field_tracker.fields,
            set2={'version'},
        )

    def test_primary_attributes(self):
        self.assertEqual(
            first=SubPluginRelease.handle_zip_file_upload,
            second=handle_sub_plugin_zip_upload,
        )
        self.assertEqual(
            first=SubPluginRelease.project_class,
            second=SubPlugin,
        )

    def test_file_name(self):
        file_name = 'test.zip'
        release = SubPluginReleaseFactory(
            zip_file=f'directory/path/{file_name}',
        )
        self.assertEqual(
            first=release.file_name,
            second=file_name,
        )

    def test__str__(self):
        release = SubPluginReleaseFactory()
        self.assertEqual(
            first=str(release),
            second=f'{release.sub_plugin} - {release.version}',
        )

    def test_clean(self):
        release = SubPluginReleaseFactory(
            version='1.0.0',
        )
        SubPluginReleaseFactory(
            sub_plugin=release.sub_plugin,
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
        sub_plugin = SubPluginFactory(
            created=original_updated,
            updated=original_updated,
        )
        release_created = original_updated + timedelta(seconds=1)
        SubPluginReleaseFactory(
            pk=None,
            sub_plugin=sub_plugin,
            created=release_created,
            version='1.0.0',
        )
        self.assertEqual(
            first=SubPlugin.objects.get(pk=sub_plugin.pk).updated,
            second=release_created,
        )

    def test_get_absolute_url(self):
        release = SubPluginReleaseFactory(zip_file='/test/this.py')
        self.assertEqual(
            first=release.get_absolute_url(),
            second=reverse(
                viewname='sub-plugin-download',
                kwargs={
                    'slug': release.sub_plugin.plugin.slug,
                    'sub_plugin_slug': release.sub_plugin.slug,
                    'zip_file': release.file_name,
                },
            ),
        )

    def test_meta_class(self):
        self.assertTrue(issubclass(SubPluginRelease.Meta, ProjectRelease.Meta))
        self.assertTupleEqual(
            tuple1=SubPluginRelease._meta.unique_together,
            tuple2=(('sub_plugin', 'version'),),
        )
        self.assertEqual(
            first=SubPluginRelease._meta.verbose_name,
            second='SubPlugin Release',
        )
        self.assertEqual(
            first=SubPluginRelease._meta.verbose_name_plural,
            second='SubPlugin Releases',
        )
