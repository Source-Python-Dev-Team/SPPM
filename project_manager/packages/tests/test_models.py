# =============================================================================
# IMPORTS
# =============================================================================
# Python
from datetime import timedelta
from random import randint, sample
from unittest import mock

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

# Third Party Django
from model_utils.tracker import FieldTracker

# App
from games.models import Game
from project_manager.common.constants import (
    FORUM_THREAD_URL,
    LOGO_MAX_HEIGHT,
    LOGO_MAX_WIDTH,
    PROJECT_BASENAME_MAX_LENGTH,
    PROJECT_SLUG_MAX_LENGTH,
)
from project_manager.common.models import (
    Project,
    ProjectContributor,
    ProjectGame,
    ProjectImage,
    ProjectRelease,
    ProjectReleaseDownloadRequirement,
    ProjectReleasePackageRequirement,
    ProjectReleasePyPiRequirement,
    ProjectReleaseVersionControlRequirement,
    ProjectTag,
)
from project_manager.common.validators import basename_validator
from project_manager.packages.constants import PACKAGE_LOGO_URL
from project_manager.packages.helpers import (
    handle_package_image_upload,
    handle_package_logo_upload,
    handle_package_zip_upload,
)
from project_manager.packages.models import (
    Package,
    PackageContributor,
    PackageGame,
    PackageImage,
    PackageRelease,
    PackageReleaseDownloadRequirement,
    PackageReleasePackageRequirement,
    PackageReleasePyPiRequirement,
    PackageReleaseVersionControlRequirement,
    PackageTag,
)
from project_manager.packages.models.abstract import (
    PackageReleaseThroughBase,
    PackageThroughBase,
)
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from tags.models import Tag
from test_utils.factories.packages import (
    PackageContributorFactory,
    PackageFactory,
    PackageGameFactory,
    PackageReleaseFactory,
    PackageReleaseDownloadRequirementFactory,
    PackageReleasePackageRequirementFactory,
    PackageReleasePyPiRequirementFactory,
    PackageReleaseVersionControlRequirementFactory,
    PackageTagFactory,
)
from test_utils.factories.requirements import (
    DownloadRequirementFactory,
    PyPiRequirementFactory,
    VersionControlRequirementFactory,
)
from test_utils.factories.users import ForumUserFactory
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class PackageReleaseThroughBaseTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageReleaseThroughBase, models.Model)
        )

    def test_id_field(self):
        field = PackageReleaseThroughBase._meta.get_field('package_release')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second='project_manager.PackageRelease',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertTrue(
            expr=PackageReleaseThroughBase._meta.abstract
        )


class PackageThroughBaseTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageThroughBase, models.Model)
        )

    def test_id_field(self):
        field = PackageThroughBase._meta.get_field('package')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second='project_manager.Package',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertTrue(
            expr=PackageThroughBase._meta.abstract
        )


class PackageTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(Package, Project)
        )

    def test_basename_field(self):
        field = Package._meta.get_field('basename')
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=PROJECT_BASENAME_MAX_LENGTH,
        )
        self.assertIn(
            member=basename_validator,
            container=field.validators,
        )
        self.assertTrue(expr=field.unique)
        self.assertTrue(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_contributors_field(self):
        field = Package._meta.get_field('contributors')
        self.assertIsInstance(
            obj=field,
            cls=models.ManyToManyField,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=ForumUser,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='package_contributions',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PackageContributor,
        )

    def test_slug_field(self):
        field = Package._meta.get_field('slug')
        self.assertIsInstance(
            obj=field,
            cls=models.SlugField,
        )
        self.assertEqual(
            first=field.max_length,
            second=PROJECT_SLUG_MAX_LENGTH,
        )
        self.assertTrue(expr=field.unique)
        self.assertTrue(expr=field.primary_key)
        self.assertTrue(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_supported_games_field(self):
        field = Package._meta.get_field('supported_games')
        self.assertIsInstance(
            obj=field,
            cls=models.ManyToManyField,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Game,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='packages',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PackageGame,
        )

    def test_tags_field(self):
        field = Package._meta.get_field('tags')
        self.assertIsInstance(
            obj=field,
            cls=models.ManyToManyField,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Tag,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='packages',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PackageTag,
        )

    def test_primary_attributes(self):
        self.assertEqual(
            first=Package.handle_logo_upload,
            second=handle_package_logo_upload,
        )
        self.assertEqual(
            first=Package.logo_path,
            second=PACKAGE_LOGO_URL,
        )

    def test__str__(self):
        package = PackageFactory()
        self.assertEqual(
            first=str(package),
            second=package.name,
        )

    def test_current_version(self):
        package = PackageFactory()
        created = now()
        for n, version in enumerate([
            '1.0.0',
            '1.0.1',
            '1.1.0',
            '1.0.9',
        ]):
            release = PackageReleaseFactory(
                package=package,
                version=version,
                created=created + timedelta(seconds=n),
            )
            self.assertEqual(
                first=package.current_version,
                second=release.version,
            )

    def test_total_downloads(self):
        package = PackageFactory()
        total_downloads = 0
        for _ in range(randint(3, 7)):
            download_count = randint(1, 20)
            total_downloads += download_count
            PackageReleaseFactory(
                package=package,
                download_count=download_count,
            )

        self.assertEqual(
            first=package.total_downloads,
            second=total_downloads,
        )

    @mock.patch(
        target='project_manager.common.models.Image.open',
    )
    def test_clean_logo(self, mock_image_open):
        Package().clean()
        mock_image_open.return_value.size = (
            LOGO_MAX_WIDTH,
            LOGO_MAX_HEIGHT,
        )
        Package(logo='test.jpg').clean()

        mock_image_open.return_value.size = (
            LOGO_MAX_WIDTH + 1,
            LOGO_MAX_HEIGHT + 1,
        )
        with self.assertRaises(ValidationError) as context:
            Package(logo='test.jpg').clean()

        self.assertEqual(
            first=len(context.exception.messages),
            second=2,
        )
        self.assertIn(
            member=f'Logo width must be no more than {LOGO_MAX_WIDTH}.',
            container=context.exception.messages,
        )
        self.assertIn(
            member=f'Logo height must be no more than {LOGO_MAX_HEIGHT}.',
            container=context.exception.messages,
        )

    @mock.patch(
        target='project_manager.common.models.settings.MEDIA_ROOT',
    )
    def test_save(self, mock_media_root):
        basename = 'test'
        mock_obj = mock.Mock(
            stem=basename,
        )
        mock_media_root.__truediv__.return_value.files.return_value = [mock_obj]
        PackageFactory(
            basename=basename,
            logo='test.jpg',
        )
        mock_obj.remove.assert_called_once_with()

    def test_get_forum_url(self):
        package = PackageFactory()
        self.assertIsNone(obj=package.get_forum_url())

        topic = randint(1, 40)
        package = PackageFactory(
            topic=topic,
        )
        self.assertEqual(
            first=package.get_forum_url(),
            second=FORUM_THREAD_URL.format(topic=topic),
        )

    def test_meta_class(self):
        self.assertTrue(issubclass(Package.Meta, Project.Meta))
        self.assertEqual(
            first=Package._meta.verbose_name,
            second='Package',
        )
        self.assertEqual(
            first=Package._meta.verbose_name_plural,
            second='Packages',
        )


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
            second=f'{release.project} - {release.version}',
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


class PackageImageTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageImage, ProjectImage)
        )

    def test_package_field(self):
        field = PackageImage._meta.get_field('package')
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
            second='images',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_primary_attributes(self):
        self.assertEqual(
            first=PackageImage.handle_image_upload,
            second=handle_package_image_upload,
        )


class PackageContributorTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageContributor, ProjectContributor)
        )
        self.assertTrue(
            expr=issubclass(PackageContributor, PackageThroughBase)
        )

    def test__str__(self):
        self.assertEqual(
            first=str(PackageContributorFactory()),
            second='Project Contributor',
        )

    def test_clean(self):
        owner = ForumUserFactory()
        contributor = ForumUserFactory()
        package = PackageFactory(owner=owner)
        PackageContributor(
            user=contributor,
            package=package,
        ).clean()

        with self.assertRaises(ValidationError) as context:
            PackageContributor(
                user=owner,
                package=package,
            ).clean()

        self.assertEqual(
            first=len(context.exception.message_dict),
            second=1,
        )
        self.assertIn(
            member='user',
            container=context.exception.message_dict,
        )
        self.assertEqual(
            first=len(context.exception.message_dict['user']),
            second=1,
        )
        self.assertEqual(
            first=context.exception.message_dict['user'][0],
            second=(
                f'{owner} is the owner and cannot be added as a contributor.'
            ),
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PackageContributor._meta.unique_together,
            tuple2=(('package', 'user'),),
        )


class PackageGameTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageGame, ProjectGame)
        )
        self.assertTrue(
            expr=issubclass(PackageGame, PackageThroughBase)
        )

    def test__str__(self):
        self.assertEqual(
            first=str(PackageGameFactory()),
            second='Project Game',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PackageGame._meta.unique_together,
            tuple2=(('package', 'game'),),
        )


class PackageTagTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageTag, ProjectTag)
        )
        self.assertTrue(
            expr=issubclass(PackageTag, PackageThroughBase)
        )

    def test__str__(self):
        self.assertEqual(
            first=str(PackageTagFactory()),
            second='Project Tag',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PackageTag._meta.unique_together,
            tuple2=(('package', 'tag'),),
        )


class PackageReleaseDownloadRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleaseDownloadRequirement,
                ProjectReleaseDownloadRequirement,
            )
        )
        self.assertTrue(
            expr=issubclass(
                PackageReleaseDownloadRequirement,
                PackageReleaseThroughBase,
            )
        )

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


class PackageReleasePackageRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleasePackageRequirement,
                ProjectReleasePackageRequirement,
            )
        )
        self.assertTrue(
            expr=issubclass(
                PackageReleasePackageRequirement,
                PackageReleaseThroughBase,
            )
        )

    def test__str__(self):
        requirement = PackageFactory()
        version = '.'.join(map(str, sample(range(100), 3)))
        self.assertEqual(
            first=str(
                PackageReleasePackageRequirementFactory(
                    package_requirement=requirement,
                    version=version,
                )
            ),
            second=f'{requirement.name} - {version}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PackageReleasePackageRequirement._meta.unique_together,
            tuple2=(('package_release', 'package_requirement'),),
        )


class PackageReleasePyPiRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleasePyPiRequirement,
                ProjectReleasePyPiRequirement,
            )
        )
        self.assertTrue(
            expr=issubclass(
                PackageReleasePyPiRequirement,
                PackageReleaseThroughBase,
            )
        )

    def test__str__(self):
        requirement = PyPiRequirementFactory()
        version = '.'.join(map(str, sample(range(100), 3)))
        self.assertEqual(
            first=str(
                PackageReleasePyPiRequirementFactory(
                    pypi_requirement=requirement,
                    version=version,
                )
            ),
            second=f'{requirement.name} - {version}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PackageReleasePyPiRequirement._meta.unique_together,
            tuple2=(('package_release', 'pypi_requirement'),),
        )


class PackageReleaseVersionControlRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleaseVersionControlRequirement,
                ProjectReleaseVersionControlRequirement,
            )
        )
        self.assertTrue(
            expr=issubclass(
                PackageReleaseVersionControlRequirement,
                PackageReleaseThroughBase,
            )
        )

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
