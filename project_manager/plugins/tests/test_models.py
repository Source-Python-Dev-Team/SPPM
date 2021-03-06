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
from model_utils.fields import AutoCreatedField
from model_utils.tracker import FieldTracker

# App
from games.models import Game
from project_manager.constants import (
    FORUM_THREAD_URL,
    LOGO_MAX_HEIGHT,
    LOGO_MAX_WIDTH,
    PROJECT_BASENAME_MAX_LENGTH,
    PROJECT_SLUG_MAX_LENGTH, RELEASE_VERSION_MAX_LENGTH,
)
from project_manager.models.abstract import (
    AbstractUUIDPrimaryKeyModel,
    Project,
    ProjectRelease,
)
from project_manager.validators import (
    basename_validator,
    version_validator,
)
from project_manager.packages.models import Package
from project_manager.plugins.constants import PLUGIN_LOGO_URL, PATH_MAX_LENGTH
from project_manager.plugins.helpers import (
    handle_plugin_image_upload,
    handle_plugin_logo_upload,
    handle_plugin_zip_upload,
)
from project_manager.plugins.models import (
    Plugin,
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginRelease,
    PluginReleaseDownloadRequirement,
    PluginReleasePackageRequirement,
    PluginReleasePyPiRequirement,
    PluginReleaseVersionControlRequirement,
    PluginTag,
    SubPluginPath,
)
from project_manager.plugins.validators import sub_plugin_path_validator
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from tags.models import Tag
from test_utils.factories.packages import PackageFactory
from test_utils.factories.plugins import (
    PluginContributorFactory,
    PluginFactory,
    PluginGameFactory,
    PluginImageFactory,
    PluginReleaseFactory,
    PluginReleaseDownloadRequirementFactory,
    PluginReleasePackageRequirementFactory,
    PluginReleasePyPiRequirementFactory,
    PluginReleaseVersionControlRequirementFactory,
    PluginTagFactory,
    SubPluginPathFactory,
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
class PluginTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(Plugin, Project)
        )

    def test_basename_field(self):
        field = Plugin._meta.get_field('basename')
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
        field = Plugin._meta.get_field('owner')
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
            second='plugins',
        )
        self.assertFalse(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_contributors_field(self):
        field = Plugin._meta.get_field('contributors')
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
            second='plugin_contributions',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PluginContributor,
        )

    def test_slug_field(self):
        field = Plugin._meta.get_field('slug')
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
        field = Plugin._meta.get_field('supported_games')
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
            second='plugins',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PluginGame,
        )

    def test_tags_field(self):
        field = Plugin._meta.get_field('tags')
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
            second='plugins',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=PluginTag,
        )

    def test_primary_attributes(self):
        self.assertEqual(
            first=Plugin.handle_logo_upload,
            second=handle_plugin_logo_upload
        )
        self.assertEqual(
            first=Plugin.logo_path,
            second=PLUGIN_LOGO_URL,
        )

    def test__str__(self):
        plugin = PluginFactory()
        self.assertEqual(
            first=str(plugin),
            second=plugin.name,
        )

    def test_current_version(self):
        plugin = PluginFactory()
        created = now()
        for n, version in enumerate([
            '1.0.0',
            '1.0.1',
            '1.1.0',
            '1.0.9',
        ]):
            release = PluginReleaseFactory(
                plugin=plugin,
                version=version,
                created=created + timedelta(seconds=n),
            )
            self.assertEqual(
                first=plugin.current_version,
                second=release.version,
            )

    def test_total_downloads(self):
        plugin = PluginFactory()
        total_downloads = 0
        for _ in range(randint(3, 7)):
            download_count = randint(1, 20)
            total_downloads += download_count
            PluginReleaseFactory(
                plugin=plugin,
                download_count=download_count,
            )

        self.assertEqual(
            first=plugin.total_downloads,
            second=total_downloads,
        )

    @mock.patch(
        target='project_manager.models.abstract.Image.open',
    )
    def test_clean_logo(self, mock_image_open):
        Plugin().clean()
        mock_image_open.return_value.size = (
            LOGO_MAX_WIDTH,
            LOGO_MAX_HEIGHT,
        )
        Plugin(logo='test.jpg').clean()

        mock_image_open.return_value.size = (
            LOGO_MAX_WIDTH + 1,
            LOGO_MAX_HEIGHT + 1,
        )
        with self.assertRaises(ValidationError) as context:
            Plugin(logo='test.jpg').clean()

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
        PluginFactory(
            basename=basename,
            logo='test.jpg',
        )
        mock_obj.remove.assert_called_once_with()

    def test_get_forum_url(self):
        plugin = PluginFactory()
        self.assertIsNone(obj=plugin.get_forum_url())

        topic = randint(1, 40)
        plugin = PluginFactory(
            topic=topic,
        )
        self.assertEqual(
            first=plugin.get_forum_url(),
            second=FORUM_THREAD_URL.format(topic=topic),
        )

    def test_get_absolute_url(self):
        plugin = PluginFactory()
        self.assertEqual(
            first=plugin.get_absolute_url(),
            second=reverse(
                viewname='plugins:detail',
                kwargs={
                    'slug': plugin.slug,
                }
            )
        )

    def test_meta_class(self):
        self.assertTrue(issubclass(Plugin.Meta, Project.Meta))
        self.assertEqual(
            first=Plugin._meta.verbose_name,
            second='Plugin',
        )
        self.assertEqual(
            first=Plugin._meta.verbose_name_plural,
            second='Plugins',
        )


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
        release_created = original_updated + timedelta(seconds=1)
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


class PluginImageTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginImage, AbstractUUIDPrimaryKeyModel)
        )

    def test_plugin_field(self):
        field = PluginImage._meta.get_field('plugin')
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
            second='images',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_image_field(self):
        field = PluginImage._meta.get_field('image')
        self.assertIsInstance(
            obj=field,
            cls=models.ImageField,
        )
        self.assertEqual(
            first=field.upload_to,
            second=handle_plugin_image_upload,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_created_field(self):
        field = PluginImage._meta.get_field('created')
        self.assertIsInstance(
            obj=field,
            cls=AutoCreatedField,
        )
        self.assertEqual(
            first=field.verbose_name,
            second='created',
        )

    def test__str__(self):
        obj = PluginImageFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.plugin} - {obj.image}',
        )

    def test_meta_class(self):
        self.assertEqual(
            first=PluginImage._meta.verbose_name,
            second='Plugin Image',
        )
        self.assertEqual(
            first=PluginImage._meta.verbose_name_plural,
            second='Plugin Images',
        )


class PluginContributorTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginContributor, AbstractUUIDPrimaryKeyModel)
        )

    def test_plugin_field(self):
        field = PluginContributor._meta.get_field('plugin')
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
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_user_field(self):
        field = PluginContributor._meta.get_field('user')
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
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = PluginContributorFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.plugin} Contributor: {obj.user}',
        )

    def test_clean(self):
        owner = ForumUserFactory()
        contributor = ForumUserFactory()
        plugin = PluginFactory(owner=owner)
        PluginContributor(
            user=contributor,
            plugin=plugin,
        ).clean()

        with self.assertRaises(ValidationError) as context:
            PluginContributor(
                user=owner,
                plugin=plugin,
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
            tuple1=PluginContributor._meta.unique_together,
            tuple2=(('plugin', 'user'),),
        )
        self.assertEqual(
            first=PluginContributor._meta.verbose_name,
            second='Plugin Contributor',
        )
        self.assertEqual(
            first=PluginContributor._meta.verbose_name_plural,
            second='Plugin Contributors',
        )


class PluginGameTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginGame, AbstractUUIDPrimaryKeyModel)
        )

    def test_plugin_field(self):
        field = PluginGame._meta.get_field('plugin')
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
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_game_field(self):
        field = PluginGame._meta.get_field('game')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Game,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = PluginGameFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.plugin} Game: {obj.game}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PluginGame._meta.unique_together,
            tuple2=(('plugin', 'game'),),
        )
        self.assertEqual(
            first=PluginGame._meta.verbose_name,
            second='Plugin Game',
        )
        self.assertEqual(
            first=PluginGame._meta.verbose_name_plural,
            second='Plugin Games',
        )


class PluginTagTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginTag, AbstractUUIDPrimaryKeyModel)
        )

    def test_plugin_field(self):
        field = PluginTag._meta.get_field('plugin')
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
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_tag_field(self):
        field = PluginTag._meta.get_field('tag')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Tag,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test__str__(self):
        obj = PluginTagFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.plugin} Tag: {obj.tag}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PluginTag._meta.unique_together,
            tuple2=(('plugin', 'tag'),),
        )
        self.assertEqual(
            first=PluginTag._meta.verbose_name,
            second='Plugin Tag',
        )
        self.assertEqual(
            first=PluginTag._meta.verbose_name_plural,
            second='Plugin Tags',
        )


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


class PluginReleasePyPiRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleasePyPiRequirement,
                AbstractUUIDPrimaryKeyModel,
            )
        )

    def test_plugin_release_field(self):
        field = PluginReleasePyPiRequirement._meta.get_field('plugin_release')
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

    def test_pypi_requirement_field(self):
        field = PluginReleasePyPiRequirement._meta.get_field(
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
        field = PluginReleasePyPiRequirement._meta.get_field('version')
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
                'plugin.'
            )
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_optional_field(self):
        field = PluginReleasePyPiRequirement._meta.get_field('optional')
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
                PluginReleasePyPiRequirementFactory(
                    pypi_requirement=requirement,
                    version=version,
                )
            ),
            second=f'{requirement.name} - {version}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PluginReleasePyPiRequirement._meta.unique_together,
            tuple2=(('plugin_release', 'pypi_requirement'),),
        )
        self.assertEqual(
            first=PluginReleasePyPiRequirement._meta.verbose_name,
            second='Plugin Release PyPi Requirement',
        )
        self.assertEqual(
            first=PluginReleasePyPiRequirement._meta.verbose_name_plural,
            second='Plugin Release PyPi Requirements',
        )


class PluginReleaseVersionControlRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleaseVersionControlRequirement,
                AbstractUUIDPrimaryKeyModel,
            )
        )

    def test_plugin_release_field(self):
        field = PluginReleaseVersionControlRequirement._meta.get_field('plugin_release')
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

    def test_vcs_requirement_field(self):
        field = PluginReleaseVersionControlRequirement._meta.get_field(
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
        field = PluginReleaseVersionControlRequirement._meta.get_field(
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
                'plugin.'
            )
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_optional_field(self):
        field = PluginReleaseVersionControlRequirement._meta.get_field(
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
                PluginReleaseVersionControlRequirementFactory(
                    vcs_requirement=requirement,
                    version=version,
                )
            ),
            second=f'{requirement.url} - {version}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=PluginReleaseVersionControlRequirement._meta.unique_together,
            tuple2=(('plugin_release', 'vcs_requirement'),),
        )
        self.assertEqual(
            first=PluginReleaseVersionControlRequirement._meta.verbose_name,
            second='Plugin Release Version Control Requirement',
        )
        self.assertEqual(
            first=PluginReleaseVersionControlRequirement._meta.verbose_name_plural,
            second='Plugin Release Version Control Requirements',
        )


class SubPluginPathTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginPath, AbstractUUIDPrimaryKeyModel))

    def test_plugin_field(self):
        field = SubPluginPath._meta.get_field('plugin')
        self.assertIsInstance(
            obj=field,
            cls=models.ForeignKey,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=Plugin,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='paths',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )

    def test_path_field(self):
        field = SubPluginPath._meta.get_field('path')
        self.assertIsInstance(obj=field, cls=models.CharField)
        self.assertEqual(
            first=field.max_length,
            second=PATH_MAX_LENGTH,
        )
        self.assertIn(
            member=sub_plugin_path_validator,
            container=field.validators,
        )

    def test_allow_module_field(self):
        field = SubPluginPath._meta.get_field('allow_module')
        self.assertIsInstance(obj=field, cls=models.BooleanField)
        self.assertFalse(expr=field.default)

    def test_allow_package_using_basename_field(self):
        field = SubPluginPath._meta.get_field('allow_package_using_basename')
        self.assertIsInstance(obj=field, cls=models.BooleanField)
        self.assertFalse(expr=field.default)

    def test_allow_package_using_init_field(self):
        field = SubPluginPath._meta.get_field('allow_package_using_init')
        self.assertIsInstance(obj=field, cls=models.BooleanField)
        self.assertFalse(expr=field.default)

    def test__str__(self):
        path = SubPluginPathFactory()
        self.assertEqual(
            first=str(path),
            second=path.path,
        )

    def test_clean(self):
        SubPluginPath(
            allow_module=True,
            allow_package_using_basename=False,
            allow_package_using_init=False,
        ).clean()
        SubPluginPath(
            allow_module=False,
            allow_package_using_basename=True,
            allow_package_using_init=False,
        ).clean()
        SubPluginPath(
            allow_module=False,
            allow_package_using_basename=False,
            allow_package_using_init=True,
        ).clean()
        with self.assertRaises(ValidationError) as context:
            SubPluginPath(
                allow_module=False,
                allow_package_using_basename=False,
                allow_package_using_init=False,
            ).clean()

        self.assertEqual(
            first=len(context.exception.message_dict),
            second=3,
        )
        for attribute in (
            'allow_module',
            'allow_package_using_basename',
            'allow_package_using_init',
        ):
            self.assertIn(
                member=attribute,
                container=context.exception.message_dict,
            )
            self.assertEqual(
                first=len(context.exception.message_dict[attribute]),
                second=1,
            )
            self.assertEqual(
                first=context.exception.message_dict[attribute][0],
                second='At least one of the "Allow" fields must be True.',
            )

        plugin = PluginFactory()
        path_1 = SubPluginPathFactory(
            path='path_1',
            plugin=plugin,
            allow_module=True,
        )
        SubPluginPathFactory(
            path='path_2',
            plugin=plugin,
        )

        path_1.path = 'path_3'
        path_1.clean()

        path_1.path = 'path_2'
        with self.assertRaises(ValidationError) as context:
            path_1.clean()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={'path': ['Path already exists for plugin.']}
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=SubPluginPath._meta.unique_together,
            tuple2=(('path', 'plugin'),),
        )
        self.assertEqual(
            first=SubPluginPath._meta.verbose_name,
            second='SubPlugin Path',
        )
        self.assertEqual(
            first=SubPluginPath._meta.verbose_name_plural,
            second='SubPlugin Paths',
        )
