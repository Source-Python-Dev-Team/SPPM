# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from rest_framework import status
from rest_framework.parsers import ParseError
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
from project_manager.sub_plugins.api.filtersets import SubPluginFilterSet
from project_manager.sub_plugins.api.serializers import (
    SubPluginContributorSerializer,
    SubPluginCreateSerializer,
    SubPluginGameSerializer,
    SubPluginImageSerializer,
    SubPluginReleaseSerializer,
    SubPluginSerializer,
    SubPluginTagSerializer,
)
from project_manager.sub_plugins.api.views import (
    SubPluginAPIView,
    SubPluginContributorViewSet,
    SubPluginGameViewSet,
    SubPluginImageViewSet,
    SubPluginReleaseViewSet,
    SubPluginTagViewSet,
    SubPluginViewSet,
)
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginContributor,
    SubPluginGame,
    SubPluginImage,
    SubPluginRelease,
    SubPluginReleaseDownloadRequirement,
    SubPluginReleasePackageRequirement,
    SubPluginReleasePyPiRequirement,
    SubPluginReleaseVersionControlRequirement,
    SubPluginTag,
)
from test_utils.factories.plugins import PluginFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginAPIViewTestCase(APITestCase):
    def test_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginAPIView, ProjectAPIView))

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginAPIView.project_type,
            second='sub-plugin',
        )

    def test_get(self):
        response = self.client.get(path='/api/sub-plugins/')
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        base_path = reverse(
            viewname=f'api:sub-plugins:endpoints',
            request=response.wsgi_request,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'contributors': base_path + f'contributors/<plugin>/<sub-plugin>/',
                'games': base_path + f'games/<plugin>/<sub-plugin>/',
                'images': base_path + f'images/<plugin>/<sub-plugin>/',
                'projects': base_path + f'projects/<plugin>/',
                'releases': base_path + f'releases/<plugin>/<sub-plugin>/',
                'tags': base_path + f'tags/<plugin>/<sub-plugin>/',
            }
        )


class SubPluginContributorViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginContributorViewSet,
                ProjectContributorViewSet,
            ),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginContributorViewSet.serializer_class,
            second=SubPluginContributorSerializer,
        )
        self.assertEqual(
            first=SubPluginContributorViewSet.project_type,
            second='sub-plugin',
        )
        self.assertEqual(
            first=SubPluginContributorViewSet.project_model,
            second=SubPlugin,
        )
        self.assertIs(
            expr1=SubPluginContributorViewSet.queryset.model,
            expr2=SubPluginContributor,
        )
        self.assertDictEqual(
            d1=SubPluginContributorViewSet.queryset.query.select_related,
            d2={'user': {'user': {}}, 'sub_plugin': {}}
        )


class SubPluginGameViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginGameViewSet, ProjectGameViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginGameViewSet.serializer_class,
            second=SubPluginGameSerializer,
        )
        self.assertEqual(
            first=SubPluginGameViewSet.project_type,
            second='sub-plugin',
        )
        self.assertEqual(
            first=SubPluginGameViewSet.project_model,
            second=SubPlugin,
        )
        self.assertIs(
            expr1=SubPluginGameViewSet.queryset.model,
            expr2=SubPluginGame,
        )
        self.assertDictEqual(
            d1=SubPluginGameViewSet.queryset.query.select_related,
            d2={'game': {}, 'sub_plugin': {}}
        )


class SubPluginImageViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginImageViewSet, ProjectImageViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginImageViewSet.serializer_class,
            second=SubPluginImageSerializer,
        )
        self.assertEqual(
            first=SubPluginImageViewSet.project_type,
            second='sub-plugin',
        )
        self.assertEqual(
            first=SubPluginImageViewSet.project_model,
            second=SubPlugin,
        )
        self.assertIs(
            expr1=SubPluginImageViewSet.queryset.model,
            expr2=SubPluginImage,
        )
        self.assertDictEqual(
            d1=SubPluginImageViewSet.queryset.query.select_related,
            d2={'sub_plugin': {}},
        )

    def test_parent_project(self):
        obj = SubPluginImageViewSet()
        invalid_slug = 'invalid'
        obj.kwargs = {'plugin_slug': invalid_slug}
        with self.assertRaises(ParseError) as context:
            _ = obj.parent_project

        self.assertEqual(
            first=context.exception.detail,
            second=f"Plugin '{invalid_slug}' not found.",
        )

        plugin = PluginFactory()
        obj.kwargs = {'plugin_slug': plugin.slug}
        self.assertEqual(
            first=obj.parent_project,
            second=plugin,
        )

    def test_get_project_kwargs(self):
        obj = SubPluginImageViewSet()
        plugin = PluginFactory()
        sub_plugin_slug = 'test-sub-plugin'
        obj.kwargs = {
            'sub_plugin_slug': sub_plugin_slug,
            'plugin_slug': plugin.slug,
        }
        self.assertDictEqual(
            d1=obj.get_project_kwargs(),
            d2={
                'slug': sub_plugin_slug,
                'plugin': plugin,
            }
        )


class SubPluginReleaseViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginReleaseViewSet, ProjectReleaseViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginReleaseViewSet.serializer_class,
            second=SubPluginReleaseSerializer,
        )
        self.assertEqual(
            first=SubPluginReleaseViewSet.project_type,
            second='sub-plugin',
        )
        self.assertEqual(
            first=SubPluginReleaseViewSet.project_model,
            second=SubPlugin,
        )
        self.assertIs(
            expr1=SubPluginReleaseViewSet.queryset.model,
            expr2=SubPluginRelease,
        )
        self.assertDictEqual(
            d1=SubPluginReleaseViewSet.queryset.query.select_related,
            d2={'sub_plugin': {}},
        )
        prefetch_lookups = SubPluginReleaseViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=4)

        lookup = prefetch_lookups[0]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='subpluginreleasepackagerequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=SubPluginReleasePackageRequirement,
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
            second='subpluginreleasedownloadrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=SubPluginReleaseDownloadRequirement,
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
            second='subpluginreleasepypirequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=SubPluginReleasePyPiRequirement,
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
            second='subpluginreleaseversioncontrolrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=SubPluginReleaseVersionControlRequirement,
        )
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('vcs_requirement__url',),
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'vcs_requirement': {}},
        )

    def test_parent_project(self):
        obj = SubPluginReleaseViewSet()
        invalid_slug = 'invalid'
        obj.kwargs = {'plugin_slug': invalid_slug}
        with self.assertRaises(ParseError) as context:
            _ = obj.parent_project

        self.assertEqual(
            first=context.exception.detail,
            second=f"Plugin '{invalid_slug}' not found.",
        )

        plugin = PluginFactory()
        obj.kwargs = {'plugin_slug': plugin.slug}
        self.assertEqual(
            first=obj.parent_project,
            second=plugin,
        )

    def test_get_project_kwargs(self):
        obj = SubPluginReleaseViewSet()
        plugin = PluginFactory()
        sub_plugin_slug = 'test-sub-plugin'
        obj.kwargs = {
            'sub_plugin_slug': sub_plugin_slug,
            'plugin_slug': plugin.slug,
        }
        self.assertDictEqual(
            d1=obj.get_project_kwargs(),
            d2={
                'slug': sub_plugin_slug,
                'plugin': plugin,
            }
        )


class SubPluginTagViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginTagViewSet, ProjectTagViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginTagViewSet.serializer_class,
            second=SubPluginTagSerializer,
        )
        self.assertEqual(
            first=SubPluginTagViewSet.project_type,
            second='sub-plugin',
        )
        self.assertEqual(
            first=SubPluginTagViewSet.project_model,
            second=SubPlugin,
        )
        self.assertIs(
            expr1=SubPluginTagViewSet.queryset.model,
            expr2=SubPluginTag,
        )
        self.assertDictEqual(
            d1=SubPluginTagViewSet.queryset.query.select_related,
            d2={'tag': {}, 'sub_plugin': {}}
        )


class SubPluginViewSetTestCase(TestCase):
    def test_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginViewSet, ProjectViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginViewSet.filterset_class,
            second=SubPluginFilterSet,
        )
        self.assertEqual(
            first=SubPluginViewSet.serializer_class,
            second=SubPluginSerializer,
        )
        self.assertEqual(
            first=SubPluginViewSet.creation_serializer_class,
            second=SubPluginCreateSerializer,
        )
        self.assertIs(expr1=SubPluginViewSet.queryset.model, expr2=SubPlugin)
        prefetch_lookups = SubPluginViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=1)
        lookup = prefetch_lookups[0]
        self.assertEqual(first=lookup.prefetch_to, second='releases')
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('-created',),
        )
        self.assertDictEqual(
            d1=SubPluginViewSet.queryset.query.select_related,
            d2={'owner': {'user': {}}, 'plugin': {}},
        )

    def test_get_queryset(self):
        with self.assertRaises(ParseError) as context:
            obj = SubPluginViewSet()
            obj.kwargs = {}
            obj.get_queryset()

        self.assertEqual(
            first=context.exception.detail,
            second='Invalid plugin_slug.',
        )

        # TODO: validate the query returns the correct data
        plugin = PluginFactory()
        obj.kwargs = {'plugin_slug': plugin.slug}
        obj.get_queryset()

        # TODO: validate the query returns the correct data
        obj.kwargs = {}
        obj.plugin = plugin
        obj.get_queryset()
