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
@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'fixtures')
class PluginReleaseDownloadViewTestCase(TestCase):

    basename = plugin = zip_file = None

    @classmethod
    def setUpTestData(cls):
        cls.basename = 'test_plugin'
        cls.plugin = PluginFactory(
            basename=cls.basename,
        )
        version = '1.0.0'
        cls.zip_file = f'{cls.plugin.slug}-v{version}.zip'
        cls.release = PluginReleaseFactory(
            plugin=cls.plugin,
            version=version,
            zip_file=cls.zip_file,
        )
        cls.api_path = f'/media/{PLUGIN_RELEASE_URL}{cls.plugin.slug}/{cls.zip_file}'

    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginReleaseDownloadView, DownloadMixin),
        )

    def test__allowed_methods(self):
        self.assertListEqual(
            list1=PluginReleaseDownloadView()._allowed_methods(),
            list2=['GET', 'OPTIONS'],
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
    def test_get_failure(self, mock_full_path):
        mock_full_path.isfile.return_value = False
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        mock_full_path.isfile.assert_called_once_with()

    def test_get_success(self):
        self.assertEqual(
            first=PluginRelease.objects.get(pk=self.release.pk).download_count,
            second=0,
        )
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertIn(
            member=(
                f'addons/source-python/plugins/{self.basename}/{self.basename}.py'
            ),
            container=str(response.content),
        )
        self.assertIn(
            member=(
                f'addons/source-python/plugins/{self.basename}/__init__.py'
            ),
            container=str(response.content),
        )
        self.assertEqual(
            first=PluginRelease.objects.get(pk=self.release.pk).download_count,
            second=1,
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
