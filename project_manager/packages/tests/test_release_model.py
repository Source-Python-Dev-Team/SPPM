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
from project_manager.packages.helpers import handle_package_zip_upload
from project_manager.packages.models import (
    Package,
    PackageRelease,
    PackageReleaseDownloadRequirement,
    PackageReleasePackageRequirement,
    PackageReleasePyPiRequirement,
    PackageReleaseVersionControlRequirement,
)
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from test_utils.factories.packages import (
    PackageFactory,
    PackageReleaseFactory,
)
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class PackageReleaseTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageRelease, ProjectRelease)
        )

    def test_package_field(self):
        field = PackageRelease._meta.get_field('package')
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
            second='releases',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_created_by_field(self):
        field = PackageRelease._meta.get_field('created_by')
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
            second='package_releases',
        )
        self.assertFalse(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_download_requirements_field(self):
        field = PackageRelease._meta.get_field('download_requirements')
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
            second='required_in_package_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PackageReleaseDownloadRequirement,
        )

    def test_package_requirements_field(self):
        field = PackageRelease._meta.get_field('package_requirements')
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
            second='required_in_package_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PackageReleasePackageRequirement,
        )

    def test_pypi_requirements_field(self):
        field = PackageRelease._meta.get_field('pypi_requirements')
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
            second='required_in_package_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PackageReleasePyPiRequirement,
        )

    def test_vcs_requirements_field(self):
        field = PackageRelease._meta.get_field('vcs_requirements')
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
            second='required_in_package_releases',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PackageReleaseVersionControlRequirement,
        )

    def test_field_tracker(self):
        self.assertTrue(expr=hasattr(PackageRelease, 'field_tracker'))
        self.assertIsInstance(
            obj=PackageRelease.field_tracker,
            cls=FieldTracker,
        )
        self.assertSetEqual(
            set1=PackageRelease.field_tracker.fields,
            set2={'version'},
        )

    def test_primary_attributes(self):
        self.assertEqual(
            first=PackageRelease.handle_zip_file_upload,
            second=handle_package_zip_upload,
        )
        self.assertEqual(
            first=PackageRelease.project_class,
            second=Package,
        )

    def test_file_name(self):
        file_name = 'test.zip'
        release = PackageReleaseFactory(
            zip_file=f'directory/path/{file_name}',
        )
        self.assertEqual(
            first=release.file_name,
            second=file_name,
        )

    def test__str__(self):
        release = PackageReleaseFactory()
        self.assertEqual(
            first=str(release),
            second=f'{release.package} - {release.version}',
        )

    def test_clean(self):
        release = PackageReleaseFactory(
            version='1.0.0',
        )
        PackageReleaseFactory(
            package=release.package,
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
        package = PackageFactory(
            created=original_updated,
            updated=original_updated,
        )
        release_created = original_updated + timedelta(seconds=1)
        PackageReleaseFactory(
            pk=None,
            package=package,
            created=release_created,
            version='1.0.0',
        )
        self.assertEqual(
            first=Package.objects.get(pk=package.pk).updated,
            second=release_created,
        )

    def test_get_absolute_url(self):
        release = PackageReleaseFactory(zip_file='/test/this.py')
        self.assertEqual(
            first=release.get_absolute_url(),
            second=reverse(
                viewname='package-download',
                kwargs={
                    'slug': release.package.slug,
                    'zip_file': release.file_name,
                },
            ),
        )

    def test_meta_class(self):
        self.assertTrue(issubclass(PackageRelease.Meta, ProjectRelease.Meta))
        self.assertTupleEqual(
            tuple1=PackageRelease._meta.unique_together,
            tuple2=(('package', 'version'),),
        )
        self.assertEqual(
            first=PackageRelease._meta.verbose_name,
            second='Package Release',
        )
        self.assertEqual(
            first=PackageRelease._meta.verbose_name_plural,
            second='Package Releases',
        )
