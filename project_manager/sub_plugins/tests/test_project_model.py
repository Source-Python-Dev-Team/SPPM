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
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.constants import SUB_PLUGIN_LOGO_URL
from project_manager.sub_plugins.helpers import handle_sub_plugin_logo_upload
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginContributor,
    SubPluginGame,
    SubPluginTag,
)
from tags.models import Tag
from test_utils.factories.sub_plugins import (
    SubPluginFactory,
    SubPluginReleaseFactory,
)
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
        for offset, version in enumerate([
            '1.0.0',
            '1.0.1',
            '1.1.0',
            '1.0.9',
        ]):
            release = SubPluginReleaseFactory(
                sub_plugin=sub_plugin,
                version=version,
                created=created + timedelta(minutes=offset),
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
