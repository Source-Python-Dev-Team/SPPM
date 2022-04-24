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
from project_manager.mixins import DownloadMixin
from project_manager.packages.constants import PACKAGE_RELEASE_URL
from project_manager.packages.models import Package, PackageRelease
from project_manager.packages.views import PackageReleaseDownloadView
from test_utils.factories.packages import PackageFactory, PackageReleaseFactory


# =============================================================================
# TEST CASES
# =============================================================================
@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'fixtures')
class PackageReleaseDownloadViewTestCase(TestCase):

    basename = package = zip_file = None

    @classmethod
    def setUpTestData(cls):
        cls.basename = 'test_package'
        cls.package = PackageFactory(
            basename=cls.basename,
        )
        version = '1.0.0'
        cls.zip_file = f'{cls.package.slug}-v{version}.zip'
        cls.release = PackageReleaseFactory(
            package=cls.package,
            version=version,
            zip_file=cls.zip_file,
        )
        cls.api_path = f'/media/{PACKAGE_RELEASE_URL}{cls.package.slug}/{cls.zip_file}'

    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageReleaseDownloadView, DownloadMixin),
        )

    def test__allowed_methods(self):
        self.assertListEqual(
            list1=PackageReleaseDownloadView()._allowed_methods(),
            list2=['GET', 'OPTIONS'],
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageReleaseDownloadView.model,
            second=PackageRelease,
        )
        self.assertEqual(
            first=PackageReleaseDownloadView.project_model,
            second=Package,
        )
        self.assertEqual(
            first=PackageReleaseDownloadView.model_kwarg,
            second='package',
        )
        self.assertEqual(
            first=PackageReleaseDownloadView.base_url,
            second=PACKAGE_RELEASE_URL,
        )

    @mock.patch(
        target='project_manager.mixins.DownloadMixin.full_path',
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
            first=PackageRelease.objects.get(pk=self.release.pk).download_count,
            second=0,
        )
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertIn(
            member=(
                f'addons/source-python/packages/custom/{self.basename}/__init__.py'
            ),
            container=str(response.content),
        )
        self.assertEqual(
            first=PackageRelease.objects.get(pk=self.release.pk).download_count,
            second=1,
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
