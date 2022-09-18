# =============================================================================
# IMPORTS
# =============================================================================
# Python
from datetime import timedelta
from random import randint
from unittest import mock

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

# App
from games.models import Game
from project_manager.constants import (
    FORUM_THREAD_URL,
    LOGO_MAX_HEIGHT,
    LOGO_MAX_WIDTH,
    PROJECT_BASENAME_MAX_LENGTH,
    PROJECT_SLUG_MAX_LENGTH,
)
from project_manager.models.abstract import Project
from project_manager.validators import basename_validator
from project_manager.packages.constants import PACKAGE_LOGO_URL
from project_manager.packages.helpers import handle_package_logo_upload
from project_manager.packages.models import (
    Package,
    PackageContributor,
    PackageGame,
    PackageTag,
)
from tags.models import Tag
from test_utils.factories.packages import (
    PackageFactory,
    PackageReleaseFactory,
)
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
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

    def test_owner_field(self):
        field = Package._meta.get_field('owner')
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
            second='packages',
        )
        self.assertFalse(expr=field.blank)
        self.assertTrue(expr=field.null)

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
        for offset, version in enumerate([
            '1.0.0',
            '1.0.1',
            '1.1.0',
            '1.0.9',
        ]):
            release = PackageReleaseFactory(
                package=package,
                version=version,
                created=created + timedelta(minutes=offset),
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
        target='project_manager.models.abstract.Image.open',
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
        target='project_manager.models.abstract.settings.MEDIA_ROOT',
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

    def test_get_absolute_url(self):
        package = PackageFactory()
        self.assertEqual(
            first=package.get_absolute_url(),
            second=reverse(
                viewname='packages:detail',
                kwargs={
                    'slug': package.slug,
                }
            )
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
