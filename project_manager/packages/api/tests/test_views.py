# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectReleaseViewSet,
    ProjectTagViewSet,
    ProjectViewSet,
)
from project_manager.packages.api.filtersets import PackageFilterSet
from project_manager.packages.api.serializers import (
    PackageContributorSerializer,
    PackageCreateSerializer,
    PackageGameSerializer,
    PackageImageSerializer,
    PackageReleaseSerializer,
    PackageSerializer,
    PackageTagSerializer,
)
from project_manager.packages.api.views import (
    PackageAPIView,
    PackageContributorViewSet,
    PackageGameViewSet,
    PackageImageViewSet,
    PackageReleaseViewSet,
    PackageTagViewSet,
    PackageViewSet,
)
from project_manager.packages.models import (
    Package,
    PackageContributor,
    PackageGame,
    PackageImage,
    PackageRelease,
    PackageReleaseDownloadRequirement,
    PackageReleasePackageRequirement,
    PackageReleasePyPiRequirement,
    PackageReleaseVersionControlRequirement,
    PackageTag,
)


# =============================================================================
# TEST CASES
# =============================================================================
class PackageAPIViewTestCase(APITestCase):
    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PackageAPIView, ProjectAPIView))

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageAPIView.project_type,
            second='package',
        )

    def test_get(self):
        response = self.client.get(path='/api/packages/')
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        base_path = reverse(
            viewname=f'api:packages:endpoints',
            request=response.wsgi_request,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'contributors': base_path + f'contributors/<package>/',
                'games': base_path + f'games/<package>/',
                'images': base_path + f'images/<package>/',
                'projects': base_path + f'projects/',
                'releases': base_path + f'releases/<package>/',
                'tags': base_path + f'tags/<package>/',
            }
        )


class PackageContributorViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageContributorViewSet,
                ProjectContributorViewSet,
            ),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageContributorViewSet.serializer_class,
            second=PackageContributorSerializer,
        )
        self.assertEqual(
            first=PackageContributorViewSet.project_type,
            second='package',
        )
        self.assertEqual(
            first=PackageContributorViewSet.project_model,
            second=Package,
        )
        self.assertIs(
            expr1=PackageContributorViewSet.queryset.model,
            expr2=PackageContributor,
        )
        self.assertDictEqual(
            d1=PackageContributorViewSet.queryset.query.select_related,
            d2={'user': {'user': {}}, 'package': {}}
        )


class PackageGameViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageGameViewSet, ProjectGameViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageGameViewSet.serializer_class,
            second=PackageGameSerializer,
        )
        self.assertEqual(
            first=PackageGameViewSet.project_type,
            second='package',
        )
        self.assertEqual(
            first=PackageGameViewSet.project_model,
            second=Package,
        )
        self.assertIs(
            expr1=PackageGameViewSet.queryset.model,
            expr2=PackageGame,
        )
        self.assertDictEqual(
            d1=PackageGameViewSet.queryset.query.select_related,
            d2={'game': {}, 'package': {}}
        )


class PackageImageViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageImageViewSet, ProjectImageViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageImageViewSet.serializer_class,
            second=PackageImageSerializer,
        )
        self.assertEqual(
            first=PackageImageViewSet.project_type,
            second='package',
        )
        self.assertEqual(
            first=PackageImageViewSet.project_model,
            second=Package,
        )
        self.assertIs(
            expr1=PackageImageViewSet.queryset.model,
            expr2=PackageImage,
        )
        self.assertDictEqual(
            d1=PackageImageViewSet.queryset.query.select_related,
            d2={'package': {}},
        )


class PackageReleaseViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageReleaseViewSet, ProjectReleaseViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageReleaseViewSet.serializer_class,
            second=PackageReleaseSerializer,
        )
        self.assertEqual(
            first=PackageReleaseViewSet.project_type,
            second='package',
        )
        self.assertEqual(
            first=PackageReleaseViewSet.project_model,
            second=Package,
        )
        self.assertIs(
            expr1=PackageReleaseViewSet.queryset.model,
            expr2=PackageRelease,
        )
        self.assertDictEqual(
            d1=PackageReleaseViewSet.queryset.query.select_related,
            d2={'package': {}},
        )
        prefetch_lookups = PackageReleaseViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=4)

        lookup = prefetch_lookups[0]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='packagereleasepackagerequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PackageReleasePackageRequirement,
        )
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('package_requirement__name',),
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'package_requirement': {}},
        )

        lookup = prefetch_lookups[1]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='packagereleasedownloadrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PackageReleaseDownloadRequirement,
        )
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('download_requirement__url',),
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'download_requirement': {}},
        )

        lookup = prefetch_lookups[2]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='packagereleasepypirequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PackageReleasePyPiRequirement,
        )
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('pypi_requirement__name',),
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'pypi_requirement': {}},
        )

        lookup = prefetch_lookups[3]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='packagereleaseversioncontrolrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PackageReleaseVersionControlRequirement,
        )
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('vcs_requirement__url',),
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'vcs_requirement': {}},
        )


class PackageTagViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PackageTagViewSet, ProjectTagViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageTagViewSet.serializer_class,
            second=PackageTagSerializer,
        )
        self.assertEqual(
            first=PackageTagViewSet.project_type,
            second='package',
        )
        self.assertEqual(
            first=PackageTagViewSet.project_model,
            second=Package,
        )
        self.assertIs(
            expr1=PackageTagViewSet.queryset.model,
            expr2=PackageTag,
        )
        self.assertDictEqual(
            d1=PackageTagViewSet.queryset.query.select_related,
            d2={'tag': {}, 'package': {}}
        )


class PackageViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PackageViewSet, ProjectViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageViewSet.filterset_class,
            second=PackageFilterSet,
        )
        self.assertEqual(
            first=PackageViewSet.serializer_class,
            second=PackageSerializer,
        )
        self.assertEqual(
            first=PackageViewSet.creation_serializer_class,
            second=PackageCreateSerializer,
        )
        self.assertIs(expr1=PackageViewSet.queryset.model, expr2=Package)
        prefetch_lookups = PackageViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=1)
        lookup = prefetch_lookups[0]
        self.assertEqual(first=lookup.prefetch_to, second='releases')
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('-created',),
        )
        self.assertDictEqual(
            d1=PackageViewSet.queryset.query.select_related,
            d2={'owner': {'user': {}}},
        )
