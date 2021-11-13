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
@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'fixtures')
class SubPluginReleaseDownloadViewTestCase(TestCase):

    basename = plugin_basename = sub_plugin = zip_file = None

    @classmethod
    def setUpTestData(cls):
        cls.plugin_basename = 'test_plugin'
        plugin = PluginFactory(
            basename=cls.plugin_basename,
        )
        cls.basename = 'test_sub_plugin'
        cls.sub_plugin = SubPluginFactory(
            plugin=plugin,
            basename=cls.basename,
        )
        version = '1.0.0'
        cls.zip_file = f'{cls.sub_plugin.slug}-v{version}.zip'
        cls.release = SubPluginReleaseFactory(
            sub_plugin=cls.sub_plugin,
            version=version,
            zip_file=cls.zip_file,
        )
        cls.api_path = f'/media/{SUB_PLUGIN_RELEASE_URL}{plugin.slug}/{cls.sub_plugin.slug}/{cls.zip_file}'

    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginReleaseDownloadView, DownloadMixin),
        )

    def test__allowed_methods(self):
        self.assertListEqual(
            list1=SubPluginReleaseDownloadView()._allowed_methods(),
            list2=['GET', 'OPTIONS'],
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
            first=SubPluginRelease.objects.get(pk=self.release.pk).download_count,
            second=0,
        )
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertIn(
            member=(
                f'addons/source-python/plugins/{self.plugin_basename}/sub_plugins/'
                f'{self.basename}/__init__.py'
            ),
            container=str(response.content),
        )
        self.assertIn(
            member=(
                f'addons/source-python/plugins/{self.plugin_basename}/sub_plugins/'
                f'{self.basename}/{self.basename}.py'
            ),
            container=str(response.content),
        )
        self.assertEqual(
            first=SubPluginRelease.objects.get(pk=self.release.pk).download_count,
            second=1,
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
