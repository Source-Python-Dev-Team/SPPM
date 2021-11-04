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
from project_manager.plugins.constants import PLUGIN_RELEASE_URL
from project_manager.plugins.models import Plugin, PluginRelease
from project_manager.plugins.views import PluginReleaseDownloadView
from test_utils.factories.plugins import PluginFactory, PluginReleaseFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PluginReleaseDownloadViewTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginReleaseDownloadView, DownloadMixin),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginReleaseDownloadView.model,
            second=PluginRelease,
        )
        self.assertEqual(
            first=PluginReleaseDownloadView.project_model,
            second=Plugin,
        )
        self.assertEqual(
            first=PluginReleaseDownloadView.model_kwarg,
            second='plugin',
        )
        self.assertEqual(
            first=PluginReleaseDownloadView.base_url,
            second=PLUGIN_RELEASE_URL,
        )

    @mock.patch(
        target='project_manager.common.mixins.DownloadMixin.full_path',
    )
    @override_settings(MEDIA_ROOT=settings.BASE_DIR / 'fixtures')
    def test_get_failure(self, mock_full_path):
        basename = 'test_plugin'
        plugin = PluginFactory(
            basename=basename,
        )
        version = '1.0.0'
        zip_file = f'{plugin.slug}-v{version}.zip'
        PluginReleaseFactory(
            plugin=plugin,
            version=version,
            zip_file=zip_file,
        )
        mock_full_path.isfile.return_value = False
        response = self.client.get(
            path=f'/media/{PLUGIN_RELEASE_URL}{plugin.slug}/{zip_file}'
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        mock_full_path.isfile.assert_called_once_with()

    @override_settings(MEDIA_ROOT=settings.BASE_DIR / 'fixtures')
    def test_get_success(self):
        basename = 'test_plugin'
        plugin = PluginFactory(
            basename=basename,
        )
        version = '1.0.0'
        zip_file = f'{plugin.slug}-v{version}.zip'
        release = PluginReleaseFactory(
            plugin=plugin,
            version=version,
            zip_file=zip_file,
        )
        self.assertEqual(
            first=PluginRelease.objects.get(pk=release.pk).download_count,
            second=0,
        )
        response = self.client.get(
            path=f'/media/{PLUGIN_RELEASE_URL}{plugin.slug}/{zip_file}'
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertIn(
            member=(
                f'addons/source-python/plugins/{basename}/{basename}.py'
            ),
            container=str(response.content),
        )
        self.assertIn(
            member=(
                f'addons/source-python/plugins/{basename}/__init__.py'
            ),
            container=str(response.content),
        )
        self.assertEqual(
            first=PluginRelease.objects.get(pk=release.pk).download_count,
            second=1,
        )
