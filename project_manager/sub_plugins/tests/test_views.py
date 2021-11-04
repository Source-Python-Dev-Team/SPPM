# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
from django.conf import settings
from django.test import TestCase, override_settings

# Third Party Django
from rest_framework import status

# App
from project_manager.common.mixins import DownloadMixin
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.constants import SUB_PLUGIN_RELEASE_URL
from project_manager.sub_plugins.models import SubPluginRelease
from project_manager.sub_plugins.views import SubPluginReleaseDownloadView
from test_utils.factories.plugins import PluginFactory
from test_utils.factories.sub_plugins import (
    SubPluginFactory,
    SubPluginReleaseFactory,
)


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginReleaseDownloadViewTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginReleaseDownloadView, DownloadMixin),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginReleaseDownloadView.model,
            second=SubPluginRelease,
        )
        self.assertEqual(
            first=SubPluginReleaseDownloadView.project_model,
            second=Plugin,
        )
        self.assertEqual(
            first=SubPluginReleaseDownloadView.model_kwarg,
            second='sub_plugin',
        )
        self.assertEqual(
            first=SubPluginReleaseDownloadView.base_url,
            second=SUB_PLUGIN_RELEASE_URL,
        )

    @mock.patch(
        target='project_manager.common.mixins.DownloadMixin.full_path',
    )
    @override_settings(MEDIA_ROOT=settings.BASE_DIR / 'fixtures')
    def test_get_failure(self, mock_full_path):
        plugin_basename = 'test_plugin'
        plugin = PluginFactory(
            basename=plugin_basename,
        )
        basename = 'test_sub_plugin'
        sub_plugin = SubPluginFactory(
            plugin=plugin,
            basename=basename,
        )
        version = '1.0.0'
        zip_file = f'{sub_plugin.slug}-v{version}.zip'
        SubPluginReleaseFactory(
            sub_plugin=sub_plugin,
            version=version,
            zip_file=zip_file,
        )
        mock_full_path.isfile.return_value = False
        response = self.client.get(
            path=(
                f'/media/{SUB_PLUGIN_RELEASE_URL}{plugin.slug}/'
                f'{sub_plugin.slug}/{zip_file}'
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        mock_full_path.isfile.assert_called_once_with()

    @override_settings(MEDIA_ROOT=settings.BASE_DIR / 'fixtures')
    def test_get_success(self):
        plugin_basename = 'test_plugin'
        plugin = PluginFactory(
            basename=plugin_basename,
        )
        basename = 'test_sub_plugin'
        sub_plugin = SubPluginFactory(
            plugin=plugin,
            basename=basename,
        )
        version = '1.0.0'
        zip_file = f'{sub_plugin.slug}-v{version}.zip'
        release = SubPluginReleaseFactory(
            sub_plugin=sub_plugin,
            version=version,
            zip_file=zip_file,
        )
        self.assertEqual(
            first=SubPluginRelease.objects.get(pk=release.pk).download_count,
            second=0,
        )
        response = self.client.get(
            path=(
                f'/media/{SUB_PLUGIN_RELEASE_URL}{plugin.slug}/'
                f'{sub_plugin.slug}/{zip_file}'
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertIn(
            member=(
                f'addons/source-python/plugins/{plugin_basename}/sub_plugins/'
                f'{basename}/__init__.py'
            ),
            container=str(response.content),
        )
        self.assertIn(
            member=(
                f'addons/source-python/plugins/{plugin_basename}/sub_plugins/'
                f'{basename}/{basename}.py'
            ),
            container=str(response.content),
        )
        self.assertEqual(
            first=SubPluginRelease.objects.get(pk=release.pk).download_count,
            second=1,
        )
