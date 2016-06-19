# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import IntegrityError
from django.test import TestCase

# App
from ...users.models import ForumUser
from ..models import (
    OldPluginRelease,
    Plugin,
    PluginImage,
    SubPluginPath,
)


# =============================================================================
# >> TEST CLASSES
# =============================================================================
class TestOldPluginRelease(TestCase):
    def test_plugin_is_required(self):
        self.assertRaisesMessage(
            IntegrityError,
            (
                'NOT NULL constraint failed: '
                'plugin_manager_oldpluginrelease.plugin_id'
            ),
            OldPluginRelease.objects.create,
        )


class TestPlugin(TestCase):
    def setUp(self):
        ForumUser.objects.create(username='test_user', id=1)
        Plugin.objects.create(name='Test', basename='test')

    def test_name_must_be_unique(self):
        self.assertRaises(
            IntegrityError,
            Plugin.objects.create,
            name='Test',
            basename='test2',
        )

    def test_basename_must_be_unique(self):
        self.assertRaises(
            IntegrityError,
            Plugin.objects.create,
            name='Test2',
            basename='test',
        )


class TestPluginImage(TestCase):
    def test_plugin_is_required(self):
        self.assertRaisesMessage(
            IntegrityError,
            (
                'NOT NULL constraint failed: '
                'plugin_manager_pluginimage.plugin_id'
            ),
            PluginImage.objects.create,
        )


class TestSubPluginPath(TestCase):
    def test_plugin_is_required(self):
        self.assertRaisesMessage(
            IntegrityError,
            (
                'NOT NULL constraint failed: '
                'plugin_manager_subpluginpath.plugin_id'
            ),
            SubPluginPath.objects.create,
        )
