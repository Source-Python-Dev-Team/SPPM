# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from django.views.generic import TemplateView

# Third Party Django
from rest_framework import status

# App
from project_manager.mixins import DownloadMixin
from project_manager.packages.constants import PACKAGE_RELEASE_URL
from project_manager.packages.models import Package, PackageRelease
from project_manager.packages.views import (
    PackageCreateView,
    PackageEditView,
    PackageReleaseDownloadView,
    PackageUpdateView,
    PackageView,
)
from test_utils.factories.packages import PackageFactory, PackageReleaseFactory


# =============================================================================
# TEST CASES
# =============================================================================
@override_settings(MEDIA_ROOT=settings.BASE_DIR / "fixtures")
class PackageReleaseDownloadViewTestCase(TestCase):

    basename = package = zip_file = None

    @classmethod
    def setUpTestData(cls):
        cls.basename = "test_package"
        cls.package = PackageFactory(
            basename=cls.basename,
        )
        version = "1.0.0"
        cls.zip_file = f"{cls.package.slug}-v{version}.zip"
        cls.release = PackageReleaseFactory(
            package=cls.package,
            version=version,
            zip_file=cls.zip_file,
        )
        cls.api_path = reverse(
            viewname="package-download",
            kwargs={
                "slug": cls.package.slug,
                "zip_file": cls.zip_file,
            },
        )

    def test_view_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageReleaseDownloadView, DownloadMixin),
        )

    def test__allowed_methods(self):
        self.assertListEqual(
            list1=PackageReleaseDownloadView()._allowed_methods(),
            list2=["GET", "OPTIONS"],
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
            second="package",
        )
        self.assertEqual(
            first=PackageReleaseDownloadView.base_url,
            second=PACKAGE_RELEASE_URL,
        )

    @mock.patch(
        target="project_manager.mixins.DownloadMixin.full_path",
    )
    def test_get_failure(self, mock_full_path):
        mock_full_path.is_file.return_value = False
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        mock_full_path.is_file.assert_called_once_with()

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
                f"addons/source-python/packages/custom/{self.basename}/__init__.py"
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


class PackageCreateViewTestCase(TestCase):

    api_path = reverse(
        viewname="packages:create",
    )

    def test_view_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageCreateView, TemplateView),
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PackageCreateView.http_method_names,
            tuple2=("get", "options"),
        )

    def test_template_name(self):
        self.assertEqual(
            first=PackageCreateView.template_name,
            second="create.html",
        )

    def test_get(self):
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data["view"]
        self.assertDictEqual(
            d1=data,
            d2={"title": "Create a Package"},
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )


class PackageViewTestCase(TestCase):

    def test_view_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageView, TemplateView),
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PackageView.http_method_names,
            tuple2=("get", "options"),
        )

    def test_template_name(self):
        self.assertEqual(
            first=PackageView.template_name,
            second="retrieve.html",
        )

    def test_list(self):
        response = self.client.get(
            path=reverse(
                viewname="packages:list",
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data["view"]
        self.assertDictEqual(
            d1=data,
            d2={"title": "Package Listing"},
        )

    def test_detail(self):
        package = PackageFactory()
        response = self.client.get(
            path=reverse(
                viewname="packages:detail",
                kwargs={
                    "slug": package.slug,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data["view"]
        self.assertDictEqual(
            d1=data,
            d2={
                "slug": package.slug,
                "title": package.name,
            },
        )

    def test_detail_invalid_slug(self):
        response = self.client.get(
            path=reverse(
                viewname="packages:detail",
                kwargs={
                    "slug": "invalid",
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data["view"]
        self.assertDictEqual(
            d1=data,
            d2={
                "slug": "invalid",
                "title": 'Package "invalid" not found.',
            },
        )


class PackageEditViewTestCase(TestCase):

    def test_view_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageEditView, TemplateView),
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PackageEditView.http_method_names,
            tuple2=("get", "options"),
        )

    def test_template_name(self):
        self.assertEqual(
            first=PackageEditView.template_name,
            second="edit.html",
        )

    def test_detail(self):
        package = PackageFactory()
        response = self.client.get(
            path=reverse(
                viewname="packages:edit",
                kwargs={
                    "slug": package.slug,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data["view"]
        self.assertDictEqual(
            d1=data,
            d2={
                "slug": package.slug,
                "title": f"Edit {package.name}",
            },
        )

    def test_detail_invalid_slug(self):
        response = self.client.get(
            path=reverse(
                viewname="packages:edit",
                kwargs={
                    "slug": "invalid",
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data["view"]
        self.assertDictEqual(
            d1=data,
            d2={
                "slug": "invalid",
                "title": 'Package "invalid" not found.',
            },
        )


class PackageUpdateViewTestCase(TestCase):

    def test_view_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageUpdateView, TemplateView),
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PackageUpdateView.http_method_names,
            tuple2=("get", "options"),
        )

    def test_template_name(self):
        self.assertEqual(
            first=PackageUpdateView.template_name,
            second="update.html",
        )

    def test_detail(self):
        package = PackageFactory()
        response = self.client.get(
            path=reverse(
                viewname="packages:update",
                kwargs={
                    "slug": package.slug,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data["view"]
        self.assertDictEqual(
            d1=data,
            d2={
                "slug": package.slug,
                "title": f"Update {package.name}",
            },
        )

    def test_detail_invalid_slug(self):
        response = self.client.get(
            path=reverse(
                viewname="packages:update",
                kwargs={
                    "slug": "invalid",
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data["view"]
        self.assertDictEqual(
            d1=data,
            d2={
                "slug": "invalid",
                "title": 'Package "invalid" not found.',
            },
        )
