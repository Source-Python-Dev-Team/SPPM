# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import connection, reset_queries
from django.db.models.expressions import CombinedExpression
from django.test import override_settings

# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.packages.models import PackageTag
from project_manager.plugins.models import PluginTag
from project_manager.sub_plugins.models import SubPluginTag
from tags.api.views import TagViewSet
from test_utils.factories.packages import PackageFactory, PackageTagFactory
from test_utils.factories.plugins import PluginFactory, PluginTagFactory
from test_utils.factories.sub_plugins import (
    SubPluginFactory,
    SubPluginTagFactory,
)
from test_utils.factories.tags import TagFactory


# =============================================================================
# TEST CASES
# =============================================================================
class TagViewSetTestCase(APITestCase):

    tag_1 = tag_2 = tag_3 = None
    package_1 = package_2 = None
    plugin_1 = plugin_2 = None
    sub_plugin_1 = sub_plugin_2 = None
    api_path = reverse(
        viewname='api:tags:tags-list',
    )

    @classmethod
    def setUpTestData(cls):
        cls.tag_1 = TagFactory()
        cls.tag_2 = TagFactory()
        cls.tag_3 = TagFactory()
        cls.tag_4 = TagFactory()
        cls.black_listed_tag = TagFactory(
            black_listed=True,
        )

        cls.package_1 = PackageFactory()
        cls.package_2 = PackageFactory()
        cls.plugin_1 = PluginFactory()
        cls.plugin_2 = PluginFactory()
        cls.sub_plugin_1 = SubPluginFactory(
            plugin=cls.plugin_1,
        )
        cls.sub_plugin_2 = SubPluginFactory(
            plugin=cls.plugin_1,
        )

        # tag_1 associations
        PackageTagFactory(
            package=cls.package_1,
            tag=cls.tag_1,
        )
        PluginTagFactory(
            plugin=cls.plugin_1,
            tag=cls.tag_1,
        )
        PluginTagFactory(
            plugin=cls.plugin_2,
            tag=cls.tag_1,
        )

        # tag_2 associations
        PackageTagFactory(
            package=cls.package_1,
            tag=cls.tag_2,
        )
        PackageTagFactory(
            package=cls.package_2,
            tag=cls.tag_2,
        )
        PluginTagFactory(
            plugin=cls.plugin_1,
            tag=cls.tag_2,
        )
        SubPluginTagFactory(
            sub_plugin=cls.sub_plugin_1,
            tag=cls.tag_2,
        )
        SubPluginTagFactory(
            sub_plugin=cls.sub_plugin_2,
            tag=cls.tag_2,
        )

        # tag_3 associations
        PluginTagFactory(
            plugin=cls.plugin_2,
            tag=cls.tag_3,
        )

    def test_filter_backends(self):
        self.assertTupleEqual(
            tuple1=TagViewSet.filter_backends,
            tuple2=(OrderingFilter, DjangoFilterBackend)
        )

    def test_ordering(self):
        self.assertTupleEqual(
            tuple1=TagViewSet.ordering,
            tuple2=('name',),
        )

    def test_ordering_fields(self):
        self.assertTupleEqual(
            tuple1=TagViewSet.ordering_fields,
            tuple2=('name', 'project_count'),
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=TagViewSet.http_method_names,
            tuple2=('get', 'options'),
        )

    def test_get_queryset(self):
        queryset = TagViewSet(action='retrieve').get_queryset().filter()
        self.assertFalse(expr=queryset.query.select_related)
        prefetch_lookups = getattr(queryset, '_prefetch_related_lookups')
        self.assertEqual(
            first=len(prefetch_lookups),
            second=1,
        )
        lookup = prefetch_lookups[0]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='sub_plugins',
        )
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('name',),
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'plugin': {}}
        )

        queryset = TagViewSet(action='list').get_queryset().filter()
        self.assertFalse(expr=queryset.query.select_related)
        self.assertTupleEqual(
            tuple1=getattr(queryset, '_prefetch_related_lookups'),
            tuple2=(),
        )
        annotations = queryset.query.annotations
        self.assertIn(
            member='package_count',
            container=annotations,
        )
        package_count = annotations['package_count']
        self.assertTrue(expr=package_count.distinct)
        self.assertEqual(
            first=len(package_count.source_expressions),
            second=1,
        )
        self.assertIs(
            expr1=package_count.source_expressions[0].target,
            expr2=getattr(PackageTag.package, 'field'),
        )

        self.assertIn(
            member='plugin_count',
            container=annotations,
        )
        plugin_count = annotations['plugin_count']
        self.assertTrue(expr=plugin_count.distinct)
        self.assertEqual(
            first=len(plugin_count.source_expressions),
            second=1,
        )
        self.assertIs(
            expr1=plugin_count.source_expressions[0].target,
            expr2=getattr(PluginTag.plugin, 'field'),
        )

        self.assertIn(
            member='sub_plugin_count',
            container=annotations,
        )
        sub_plugin_count = annotations['sub_plugin_count']
        self.assertTrue(expr=sub_plugin_count.distinct)
        self.assertEqual(
            first=len(sub_plugin_count.source_expressions),
            second=1,
        )
        self.assertIs(
            expr1=sub_plugin_count.source_expressions[0].target,
            expr2=getattr(SubPluginTag.sub_plugin, 'field'),
        )

        self.assertIn(
            member='project_count',
            container=annotations,
        )
        project_count = annotations['project_count']
        self.assertIsInstance(
            obj=project_count,
            cls=CombinedExpression,
        )
        self.assertEqual(
            first=project_count.connector,
            second='+',
        )
        self.assertEqual(
            first=project_count.rhs,
            second=sub_plugin_count,
        )
        lhs = project_count.lhs
        self.assertIsInstance(
            obj=lhs,
            cls=CombinedExpression,
        )
        self.assertEqual(
            first=lhs.lhs,
            second=package_count,
        )
        self.assertEqual(
            first=lhs.connector,
            second='+',
        )
        self.assertEqual(
            first=lhs.rhs,
            second=plugin_count,
        )

    @override_settings(DEBUG=True)
    def test_get_list(self):
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=len(connection.queries),
            second=2,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=4,
        )
        results = content['results']
        self.assertDictEqual(
            d1=results[0],
            d2={
                'name': self.tag_1.name,
                'package_count': 1,
                'plugin_count': 2,
                'sub_plugin_count': 0,
                'project_count': 3,
            },
        )
        self.assertDictEqual(
            d1=results[1],
            d2={
                'name': self.tag_2.name,
                'package_count': 2,
                'plugin_count': 1,
                'sub_plugin_count': 2,
                'project_count': 5,
            },
        )
        self.assertDictEqual(
            d1=results[2],
            d2={
                'name': self.tag_3.name,
                'package_count': 0,
                'plugin_count': 1,
                'sub_plugin_count': 0,
                'project_count': 1,
            },
        )
        self.assertDictEqual(
            d1=results[3],
            d2={
                'name': self.tag_4.name,
                'package_count': 0,
                'plugin_count': 0,
                'sub_plugin_count': 0,
                'project_count': 0,
            },
        )

        reset_queries()
        response = self.client.get(
            path=self.api_path,
            data={'ordering': '-project_count'},
        )
        self.assertEqual(
            first=len(connection.queries),
            second=2,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=4,
        )
        results = content['results']
        self.assertDictEqual(
            d1=results[0],
            d2={
                'name': self.tag_2.name,
                'package_count': 2,
                'plugin_count': 1,
                'sub_plugin_count': 2,
                'project_count': 5,
            },
        )
        self.assertDictEqual(
            d1=results[1],
            d2={
                'name': self.tag_1.name,
                'package_count': 1,
                'plugin_count': 2,
                'sub_plugin_count': 0,
                'project_count': 3,
            },
        )
        self.assertDictEqual(
            d1=results[2],
            d2={
                'name': self.tag_3.name,
                'package_count': 0,
                'plugin_count': 1,
                'sub_plugin_count': 0,
                'project_count': 1,
            },
        )
        self.assertDictEqual(
            d1=results[3],
            d2={
                'name': self.tag_4.name,
                'package_count': 0,
                'plugin_count': 0,
                'sub_plugin_count': 0,
                'project_count': 0,
            },
        )

    @override_settings(DEBUG=True)
    def test_get_detail(self):
        response = self.client.get(
            path=reverse(
                viewname='api:tags:tags-detail',
                kwargs={
                    'pk': self.tag_1.name,
                },
            ),
        )
        self.assertEqual(
            first=len(connection.queries),
            second=4,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'name': self.tag_1.name,
                'packages': [
                    {
                        'name': self.package_1.name,
                        'slug': self.package_1.slug,
                    },
                ],
                'plugins': [
                    {
                        'name': self.plugin_1.name,
                        'slug': self.plugin_1.slug,
                    },
                    {
                        'name': self.plugin_2.name,
                        'slug': self.plugin_2.slug,
                    },
                ],
                'sub_plugins': [],
            }
        )

        reset_queries()
        response = self.client.get(
            path=reverse(
                viewname='api:tags:tags-detail',
                kwargs={
                    'pk': self.tag_2.name,
                },
            ),
        )
        self.assertEqual(
            first=len(connection.queries),
            second=4,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'name': self.tag_2.name,
                'packages': [
                    {
                        'name': self.package_1.name,
                        'slug': self.package_1.slug,
                    },
                    {
                        'name': self.package_2.name,
                        'slug': self.package_2.slug,
                    },
                ],
                'plugins': [
                    {
                        'name': self.plugin_1.name,
                        'slug': self.plugin_1.slug,
                    },
                ],
                'sub_plugins': [
                    {
                        'name': self.sub_plugin_1.name,
                        'slug': self.sub_plugin_1.slug,
                        'plugin': {
                            'name': self.plugin_1.name,
                            'slug': self.plugin_1.slug,
                        }
                    },
                    {
                        'name': self.sub_plugin_2.name,
                        'slug': self.sub_plugin_2.slug,
                        'plugin': {
                            'name': self.plugin_1.name,
                            'slug': self.plugin_1.slug,
                        }
                    },
                ],
            }
        )

        reset_queries()
        response = self.client.get(
            path=reverse(
                viewname='api:tags:tags-detail',
                kwargs={
                    'pk': self.tag_3.name,
                },
            ),
        )
        self.assertEqual(
            first=len(connection.queries),
            second=4,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'name': self.tag_3.name,
                'packages': [],
                'plugins': [
                    {
                        'name': self.plugin_2.name,
                        'slug': self.plugin_2.slug,
                    },
                ],
                'sub_plugins': [],
            }
        )

        reset_queries()
        response = self.client.get(
            path=reverse(
                viewname='api:tags:tags-detail',
                kwargs={
                    'pk': self.tag_4.name,
                },
            ),
        )
        self.assertEqual(
            first=len(connection.queries),
            second=4,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'name': self.tag_4.name,
                'packages': [],
                'plugins': [],
                'sub_plugins': [],
            }
        )

        reset_queries()
        response = self.client.get(
            path=reverse(
                viewname='api:tags:tags-detail',
                kwargs={
                    'pk': self.black_listed_tag.name,
                },
            ),
        )
        self.assertEqual(
            first=len(connection.queries),
            second=1,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['name'],
            second='Tag List',
        )
