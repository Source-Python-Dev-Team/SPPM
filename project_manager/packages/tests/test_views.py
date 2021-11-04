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
from project_manager.packages.constants import PACKAGE_RELEASE_URL
from project_manager.packages.models import Package, PackageRelease
from project_manager.packages.views import PackageReleaseDownloadView
from test_utils.factories.packages import PackageFactory, PackageReleaseFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PackageReleaseDownloadViewTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageReleaseDownloadView, DownloadMixin),
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
        target='project_manager.common.mixins.DownloadMixin.full_path',
    )
    @override_settings(MEDIA_ROOT=settings.BASE_DIR / 'fixtures')
    def test_get_failure(self, mock_full_path):
        basename = 'test_package'
        package = PackageFactory(
            basename=basename,
        )
        version = '1.0.0'
        zip_file = f'{package.slug}-v{version}.zip'
        PackageReleaseFactory(
            package=package,
            version=version,
            zip_file=zip_file,
        )
        mock_full_path.isfile.return_value = False
        response = self.client.get(
            path=f'/media/{PACKAGE_RELEASE_URL}{package.slug}/{zip_file}'
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        mock_full_path.isfile.assert_called_once_with()

    @override_settings(MEDIA_ROOT=settings.BASE_DIR / 'fixtures')
    def test_get_success(self):
        basename = 'test_package'
        package = PackageFactory(
            basename=basename,
        )
        version = '1.0.0'
        zip_file = f'{package.slug}-v{version}.zip'
        release = PackageReleaseFactory(
            package=package,
            version=version,
            zip_file=zip_file,
        )
        self.assertEqual(
            first=PackageRelease.objects.get(pk=release.pk).download_count,
            second=0,
        )
        response = self.client.get(
            path=f'/media/{PACKAGE_RELEASE_URL}{package.slug}/{zip_file}'
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertIn(
            member=(
                f'addons/source-python/packages/custom/{basename}/__init__.py'
            ),
            container=str(response.content),
        )
        self.assertEqual(
            first=PackageRelease.objects.get(pk=release.pk).download_count,
            second=1,
        )
