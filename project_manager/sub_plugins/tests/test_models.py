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
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.constants import SUB_PLUGIN_LOGO_URL
from project_manager.sub_plugins.helpers import (
    handle_sub_plugin_image_upload,
    handle_sub_plugin_logo_upload,
    handle_sub_plugin_zip_upload,
)
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginContributor,
    SubPluginGame,
    SubPluginImage,
    SubPluginRelease,
    SubPluginReleaseDownloadRequirement,
    SubPluginReleasePackageRequirement,
    SubPluginReleasePyPiRequirement,
    SubPluginReleaseVersionControlRequirement,
    SubPluginTag,
)
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from tags.models import Tag
from test_utils.factories.packages import PackageFactory
from test_utils.factories.requirements import (
    DownloadRequirementFactory,
    PyPiRequirementFactory,
    VersionControlRequirementFactory,
)
from test_utils.factories.sub_plugins import (
    SubPluginContributorFactory,
    SubPluginFactory,
    SubPluginGameFactory,
    SubPluginImageFactory,
    SubPluginReleaseFactory,
    SubPluginReleaseDownloadRequirementFactory,
    SubPluginReleasePackageRequirementFactory,
    SubPluginReleasePyPiRequirementFactory,
    SubPluginReleaseVersionControlRequirementFactory,
    SubPluginTagFactory,
)
from test_utils.factories.users import ForumUserFactory
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPlugin, Project)
        )

    def test_basename_field(self):
        field = SubPlugin._meta.get_field('basename')
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
        self.assertFalse(expr=field.unique)
        self.assertTrue(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_owner_field(self):
        field = SubPlugin._meta.get_field('owner')
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
            second='sub_plugins',
        )
        self.assertFalse(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_contributors_field(self):
        field = SubPlugin._meta.get_field('contributors')
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
            second='sub_plugin_contributions',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=SubPluginContributor,
        )

    def test_slug_field(self):
        field = SubPlugin._meta.get_field('slug')
        self.assertIsInstance(
            obj=field,
            cls=models.SlugField,
        )
        self.assertEqual(
            first=field.max_length,
            second=PROJECT_SLUG_MAX_LENGTH,
        )
        self.assertFalse(expr=field.unique)
        self.assertFalse(expr=field.primary_key)
        self.assertTrue(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_plugin_field(self):
        field = SubPlugin._meta.get_field('plugin')
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
            second='sub_plugins',
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )

    def test_supported_games_field(self):
        field = SubPlugin._meta.get_field('supported_games')
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
            second='sub_plugins',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=SubPluginGame,
        )

    def test_tags_field(self):
        field = SubPlugin._meta.get_field('tags')
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
            second='sub_plugins',
        )
        self.assertEqual(
            first=field.remote_field.through,
            second=SubPluginTag,
        )

    def test_primary_attributes(self):
        self.assertEqual(
            first=SubPlugin.handle_logo_upload,
            second=handle_sub_plugin_logo_upload
        )
        self.assertEqual(
            first=SubPlugin.logo_path,
            second=SUB_PLUGIN_LOGO_URL,
        )

    def test__str__(self):
        sub_plugin = SubPluginFactory()
        self.assertEqual(
            first=str(sub_plugin),
            second=f'{sub_plugin.plugin.name}: {sub_plugin.name}',
        )

    def test_current_version(self):
        sub_plugin = SubPluginFactory()
        created = now()
        for n, version in enumerate([
            '1.0.0',
            '1.0.1',
            '1.1.0',
            '1.0.9',
        ]):
            release = SubPluginReleaseFactory(
                sub_plugin=sub_plugin,
                version=version,
                created=created + timedelta(seconds=n),
            )
            self.assertEqual(
                first=sub_plugin.current_version,
                second=release.version,
            )

    def test_total_downloads(self):
        sub_plugin = SubPluginFactory()
        total_downloads = 0
        for _ in range(randint(3, 7)):
            download_count = randint(1, 20)
            total_downloads += download_count
            SubPluginReleaseFactory(
                sub_plugin=sub_plugin,
                download_count=download_count,
            )

        self.assertEqual(
            first=sub_plugin.total_downloads,
            second=total_downloads,
        )

    @mock.patch(
        target='project_manager.models.abstract.Image.open',
    )
    def test_clean_logo(self, mock_image_open):
        SubPlugin().clean()
        mock_image_open.return_value.size = (
            LOGO_MAX_WIDTH,
            LOGO_MAX_HEIGHT,
        )
        SubPlugin(logo='test.jpg').clean()

        mock_image_open.return_value.size = (
            LOGO_MAX_WIDTH + 1,
            LOGO_MAX_HEIGHT + 1,
        )
        with self.assertRaises(ValidationError) as context:
            SubPlugin(logo='test.jpg').clean()

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
        SubPluginFactory(
            basename=basename,
            logo='test.jpg',
        )
        mock_obj.remove.assert_called_once_with()

    def test_get_forum_url(self):
        sub_plugin = SubPluginFactory()
        self.assertIsNone(obj=sub_plugin.get_forum_url())

        topic = randint(1, 40)
        sub_plugin = SubPluginFactory(
            topic=topic,
        )
        self.assertEqual(
            first=sub_plugin.get_forum_url(),
            second=FORUM_THREAD_URL.format(topic=topic),
        )

    def test_get_absolute_url(self):
        sub_plugin = SubPluginFactory()
        self.assertEqual(
            first=sub_plugin.get_absolute_url(),
            second=reverse(
                viewname='plugins:sub-plugins:detail',
                kwargs={
                    'slug': sub_plugin.plugin_id,
                    'sub_plugin_slug': sub_plugin.slug,
                }
            )
        )

    def test_meta_class(self):
        self.assertTrue(issubclass(SubPlugin.Meta, Project.Meta))
        self.assertTupleEqual(
            tuple1=SubPlugin._meta.unique_together,
            tuple2=(
                ('plugin', 'basename'),
                ('plugin', 'name'),
                ('plugin', 'slug'),
            )
        )
        self.assertEqual(
            first=SubPlugin._meta.verbose_name,
            second='SubPlugin',
        )
        self.assertEqual(
            first=SubPlugin._meta.verbose_name_plural,
            second='SubPlugins',
        )


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


class SubPluginImageTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginImage, AbstractUUIDPrimaryKeyModel)
        )

    def test_sub_plugin_field(self):
        field = SubPluginImage._meta.get_field('sub_plugin')
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
            second='images',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_image_field(self):
        field = SubPluginImage._meta.get_field('image')
        self.assertIsInstance(
            obj=field,
            cls=models.ImageField,
        )
        self.assertEqual(
            first=field.upload_to,
            second=handle_sub_plugin_image_upload,
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_created_field(self):
        field = SubPluginImage._meta.get_field('created')
        self.assertIsInstance(
            obj=field,
            cls=AutoCreatedField,
        )
        self.assertEqual(
            first=field.verbose_name,
            second='created',
        )

    def test__str__(self):
        obj = SubPluginImageFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.sub_plugin} - {obj.image}',
        )

    def test_meta_class(self):
        self.assertEqual(
            first=SubPluginImage._meta.verbose_name,
            second='SubPlugin Image',
        )
        self.assertEqual(
            first=SubPluginImage._meta.verbose_name_plural,
            second='SubPlugin Images',
        )


class SubPluginContributorTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginContributor, AbstractUUIDPrimaryKeyModel)
        )

    def test_sub_plugin_field(self):
        field = SubPluginContributor._meta.get_field('sub_plugin')
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
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_user_field(self):
        field = SubPluginContributor._meta.get_field('user')
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
        obj = SubPluginContributorFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.sub_plugin} Contributor: {obj.user}',
        )

    def test_clean(self):
        owner = ForumUserFactory()
        contributor = ForumUserFactory()
        sub_plugin = SubPluginFactory(owner=owner)
        SubPluginContributor(
            user=contributor,
            sub_plugin=sub_plugin,
        ).clean()

        with self.assertRaises(ValidationError) as context:
            SubPluginContributor(
                user=owner,
                sub_plugin=sub_plugin,
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
            tuple1=SubPluginContributor._meta.unique_together,
            tuple2=(('sub_plugin', 'user'),),
        )
        self.assertEqual(
            first=SubPluginContributor._meta.verbose_name,
            second='SubPlugin Contributor',
        )
        self.assertEqual(
            first=SubPluginContributor._meta.verbose_name_plural,
            second='SubPlugin Contributors',
        )


class SubPluginGameTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginGame, AbstractUUIDPrimaryKeyModel)
        )

    def test_sub_plugin_field(self):
        field = SubPluginGame._meta.get_field('sub_plugin')
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
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_game_field(self):
        field = SubPluginGame._meta.get_field('game')
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
        obj = SubPluginGameFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.sub_plugin} Game: {obj.game}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=SubPluginGame._meta.unique_together,
            tuple2=(('sub_plugin', 'game'),),
        )
        self.assertEqual(
            first=SubPluginGame._meta.verbose_name,
            second='SubPlugin Game',
        )
        self.assertEqual(
            first=SubPluginGame._meta.verbose_name_plural,
            second='SubPlugin Games',
        )


class SubPluginTagTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginTag, AbstractUUIDPrimaryKeyModel)
        )

    def test_sub_plugin_field(self):
        field = SubPluginTag._meta.get_field('sub_plugin')
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
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_tag_field(self):
        field = SubPluginTag._meta.get_field('tag')
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
        obj = SubPluginTagFactory()
        self.assertEqual(
            first=str(obj),
            second=f'{obj.sub_plugin} Tag: {obj.tag}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=SubPluginTag._meta.unique_together,
            tuple2=(('sub_plugin', 'tag'),),
        )
        self.assertEqual(
            first=SubPluginTag._meta.verbose_name,
            second='SubPlugin Tag',
        )
        self.assertEqual(
            first=SubPluginTag._meta.verbose_name_plural,
            second='SubPlugin Tags',
        )


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


class SubPluginReleasePackageRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleasePackageRequirement,
                AbstractUUIDPrimaryKeyModel,
            )
        )

    def test_sub_plugin_release_field(self):
        field = SubPluginReleasePackageRequirement._meta.get_field('sub_plugin_release')
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

    def test_package_requirement_field(self):
        field = SubPluginReleasePackageRequirement._meta.get_field(
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
        field = SubPluginReleasePackageRequirement._meta.get_field('version')
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
                'sub_plugin.'
            )
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_optional_field(self):
        field = SubPluginReleasePackageRequirement._meta.get_field('optional')
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
                SubPluginReleasePackageRequirementFactory(
                    package_requirement=requirement,
                    version=version,
                )
            ),
            second=f'{requirement.name} - {version}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=SubPluginReleasePackageRequirement._meta.unique_together,
            tuple2=(('sub_plugin_release', 'package_requirement'),),
        )
        self.assertEqual(
            first=SubPluginReleasePackageRequirement._meta.verbose_name,
            second='SubPlugin Release Package Requirement',
        )
        self.assertEqual(
            first=SubPluginReleasePackageRequirement._meta.verbose_name_plural,
            second='SubPlugin Release Package Requirements',
        )


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


class SubPluginReleaseVersionControlRequirementTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleaseVersionControlRequirement,
                AbstractUUIDPrimaryKeyModel,
            )
        )

    def test_sub_plugin_release_field(self):
        field = SubPluginReleaseVersionControlRequirement._meta.get_field('sub_plugin_release')
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

    def test_vcs_requirement_field(self):
        field = SubPluginReleaseVersionControlRequirement._meta.get_field(
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
        field = SubPluginReleaseVersionControlRequirement._meta.get_field(
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
                'sub_plugin.'
            )
        )
        self.assertTrue(expr=field.blank)
        self.assertTrue(expr=field.null)

    def test_optional_field(self):
        field = SubPluginReleaseVersionControlRequirement._meta.get_field(
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
                SubPluginReleaseVersionControlRequirementFactory(
                    vcs_requirement=requirement,
                    version=version,
                )
            ),
            second=f'{requirement.url} - {version}',
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=SubPluginReleaseVersionControlRequirement._meta.unique_together,
            tuple2=(('sub_plugin_release', 'vcs_requirement'),),
        )
        self.assertEqual(
            first=SubPluginReleaseVersionControlRequirement._meta.verbose_name,
            second='SubPlugin Release Version Control Requirement',
        )
        self.assertEqual(
            first=SubPluginReleaseVersionControlRequirement._meta.verbose_name_plural,
            second='SubPlugin Release Version Control Requirements',
        )
