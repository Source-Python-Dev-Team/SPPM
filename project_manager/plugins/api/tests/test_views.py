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
from project_manager.common.api.views.mixins import ProjectThroughModelMixin
from project_manager.plugins.api.filtersets import PluginFilterSet
from project_manager.plugins.api.serializers import (
    PluginContributorSerializer,
    PluginCreateSerializer,
    PluginGameSerializer,
    PluginImageSerializer,
    PluginReleaseSerializer,
    PluginSerializer,
    PluginTagSerializer,
    SubPluginPathSerializer,
)
from project_manager.plugins.api.views import (
    PluginAPIView,
    PluginContributorViewSet,
    PluginGameViewSet,
    PluginImageViewSet,
    PluginReleaseViewSet,
    PluginTagViewSet,
    PluginViewSet,
    SubPluginPathViewSet,
)
from project_manager.plugins.models import (
    Plugin,
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginRelease,
    PluginReleaseDownloadRequirement,
    PluginReleasePackageRequirement,
    PluginReleasePyPiRequirement,
    PluginReleaseVersionControlRequirement,
    PluginTag,
    SubPluginPath,
)


# =============================================================================
# TEST CASES
# =============================================================================
class PluginAPIViewTestCase(APITestCase):
    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PluginAPIView, ProjectAPIView))

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginAPIView.project_type,
            second='plugin',
        )

    def test_get(self):
        response = self.client.get(path='/api/plugins/')
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        base_path = reverse(
            viewname=f'api:plugins:endpoints',
            request=response.wsgi_request,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'contributors': base_path + f'contributors/<plugin>/',
                'games': base_path + f'games/<plugin>/',
                'images': base_path + f'images/<plugin>/',
                'projects': base_path + f'projects/',
                'releases': base_path + f'releases/<plugin>/',
                'tags': base_path + f'tags/<plugin>/',
                'paths': base_path + f'paths/<plugin>/',
            }
        )


class PluginContributorViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginContributorViewSet,
                ProjectContributorViewSet,
            ),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginContributorViewSet.serializer_class,
            second=PluginContributorSerializer,
        )
        self.assertEqual(
            first=PluginContributorViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=PluginContributorViewSet.project_model,
            second=Plugin,
        )
        self.assertIs(
            expr1=PluginContributorViewSet.queryset.model,
            expr2=PluginContributor,
        )
        self.assertDictEqual(
            d1=PluginContributorViewSet.queryset.query.select_related,
            d2={'user': {'user': {}}, 'plugin': {}}
        )


class PluginGameViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginGameViewSet, ProjectGameViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginGameViewSet.serializer_class,
            second=PluginGameSerializer,
        )
        self.assertEqual(
            first=PluginGameViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=PluginGameViewSet.project_model,
            second=Plugin,
        )
        self.assertIs(
            expr1=PluginGameViewSet.queryset.model,
            expr2=PluginGame,
        )
        self.assertDictEqual(
            d1=PluginGameViewSet.queryset.query.select_related,
            d2={'game': {}, 'plugin': {}}
        )


class PluginImageViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginImageViewSet, ProjectImageViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginImageViewSet.serializer_class,
            second=PluginImageSerializer,
        )
        self.assertEqual(
            first=PluginImageViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=PluginImageViewSet.project_model,
            second=Plugin,
        )
        self.assertIs(
            expr1=PluginImageViewSet.queryset.model,
            expr2=PluginImage,
        )
        self.assertDictEqual(
            d1=PluginImageViewSet.queryset.query.select_related,
            d2={'plugin': {}},
        )


class PluginReleaseViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginReleaseViewSet, ProjectReleaseViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginReleaseViewSet.serializer_class,
            second=PluginReleaseSerializer,
        )
        self.assertEqual(
            first=PluginReleaseViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=PluginReleaseViewSet.project_model,
            second=Plugin,
        )
        self.assertIs(
            expr1=PluginReleaseViewSet.queryset.model,
            expr2=PluginRelease,
        )
        self.assertDictEqual(
            d1=PluginReleaseViewSet.queryset.query.select_related,
            d2={'plugin': {}},
        )
        prefetch_lookups = PluginReleaseViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=4)

        lookup = prefetch_lookups[0]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='pluginreleasepackagerequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PluginReleasePackageRequirement,
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
            second='pluginreleasedownloadrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PluginReleaseDownloadRequirement,
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
            second='pluginreleasepypirequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PluginReleasePyPiRequirement,
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
            second='pluginreleaseversioncontrolrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PluginReleaseVersionControlRequirement,
        )
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('vcs_requirement__url',),
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'vcs_requirement': {}},
        )


class PluginTagViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PluginTagViewSet, ProjectTagViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginTagViewSet.serializer_class,
            second=PluginTagSerializer,
        )
        self.assertEqual(
            first=PluginTagViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=PluginTagViewSet.project_model,
            second=Plugin,
        )
        self.assertIs(
            expr1=PluginTagViewSet.queryset.model,
            expr2=PluginTag,
        )
        self.assertDictEqual(
            d1=PluginTagViewSet.queryset.query.select_related,
            d2={'tag': {}, 'plugin': {}}
        )


class PluginViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PluginViewSet, ProjectViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginViewSet.filterset_class,
            second=PluginFilterSet,
        )
        self.assertEqual(
            first=PluginViewSet.serializer_class,
            second=PluginSerializer,
        )
        self.assertEqual(
            first=PluginViewSet.creation_serializer_class,
            second=PluginCreateSerializer,
        )
        self.assertIs(expr1=PluginViewSet.queryset.model, expr2=Plugin)
        prefetch_lookups = PluginViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=1)
        lookup = prefetch_lookups[0]
        self.assertEqual(first=lookup.prefetch_to, second='releases')
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('-created',),
        )
        self.assertDictEqual(
            d1=PluginViewSet.queryset.query.select_related,
            d2={'owner': {'user': {}}},
        )


class SubPluginPathViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginPathViewSet, ProjectThroughModelMixin),
        )

    def test_base_attributes(self):
        self.assertTupleEqual(
            tuple1=SubPluginPathViewSet.http_method_names,
            tuple2=('get', 'post', 'patch', 'delete', 'options'),
        )
        self.assertTupleEqual(
            tuple1=SubPluginPathViewSet.ordering,
            tuple2=('path',),
        )
        self.assertEqual(
            first=SubPluginPathViewSet.serializer_class,
            second=SubPluginPathSerializer,
        )
        self.assertEqual(
            first=SubPluginPathViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=SubPluginPathViewSet.project_model,
            second=Plugin,
        )
        self.assertEqual(
            first=SubPluginPathViewSet.related_model_type,
            second='Sub-Plugin Path',
        )
        self.assertIs(
            expr1=SubPluginPathViewSet.queryset.model,
            expr2=SubPluginPath,
        )
        self.assertDictEqual(
            d1=SubPluginPathViewSet.queryset.query.select_related,
            d2={'plugin': {}},
        )
