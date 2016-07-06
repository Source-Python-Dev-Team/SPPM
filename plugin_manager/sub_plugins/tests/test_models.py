# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import IntegrityError
from django.test import TestCase

# App
from ...plugins.models import Plugin
from ...users.models import ForumUser
from ..models import SubPluginRelease, SubPlugin, SubPluginImage


# =============================================================================
# >> TESTS
# =============================================================================
class TestSubPluginRelease(TestCase):
    def test_plugin_is_required(self):
        self.assertRaisesMessage(
            IntegrityError,
            (
                'NOT NULL constraint failed: '
                'plugin_manager_subpluginrelease.sub_plugin_id'
            ),
            SubPluginRelease.objects.create,
        )


class TestSubPlugin(TestCase):
    def setUp(self):
        ForumUser.objects.create(username='test_user', id=1)
        self.plugin = Plugin.objects.create(name='Test3', basename='test3')
        SubPlugin.objects.create(
            name='Test',
            basename='test',
            plugin=self.plugin,
        )

    def test_name_must_be_unique_for_plugin(self):
        self.assertRaises(
            IntegrityError,
            SubPlugin.objects.create,
            name='Test',
            basename='test2',
            plugin=self.plugin,
        )

    def test_basename_must_be_unique_for_plugin(self):
        self.assertRaises(
            IntegrityError,
            SubPlugin.objects.create,
            name='Test2',
            basename='test',
            plugin=self.plugin,
        )


class TestSubPluginImage(TestCase):
    def test_plugin_is_required(self):
        self.assertRaisesMessage(
            IntegrityError,
            (
                'NOT NULL constraint failed: '
                'plugin_manager_subpluginimage.sub_plugin_id'
            ),
            SubPluginImage.objects.create,
        )
