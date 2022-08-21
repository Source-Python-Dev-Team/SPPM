# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import connection, reset_queries
from django.db.models.expressions import CombinedExpression
from django.test import override_settings

# Third Party Django
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.packages.models import PackageGame
from project_manager.plugins.models import PluginGame
from project_manager.sub_plugins.models import SubPluginGame
from games.api.views import GameViewSet
from test_utils.factories.packages import PackageFactory, PackageGameFactory
from test_utils.factories.plugins import PluginFactory, PluginGameFactory
from test_utils.factories.sub_plugins import (
    SubPluginFactory,
    SubPluginGameFactory,
)
from test_utils.factories.games import GameFactory


# =============================================================================
# TEST CASES
# =============================================================================
class GameViewSetTestCase(APITestCase):

    game_1 = game_2 = game_3 = None
    package_1 = package_2 = None
    plugin_1 = plugin_2 = None
    sub_plugin_1 = sub_plugin_2 = None
    api_path = reverse(
        viewname='api:games:games-list'
    )

    @classmethod
    def setUpTestData(cls):
        cls.game_1 = GameFactory()
        cls.game_2 = GameFactory()
        cls.game_3 = GameFactory()
        cls.game_4 = GameFactory()

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

        # game_1 associations
        PackageGameFactory(
            package=cls.package_1,
            game=cls.game_1,
        )
        PluginGameFactory(
            plugin=cls.plugin_1,
            game=cls.game_1,
        )
        PluginGameFactory(
            plugin=cls.plugin_2,
            game=cls.game_1,
        )

        # game_2 associations
        PackageGameFactory(
            package=cls.package_1,
            game=cls.game_2,
        )
        PackageGameFactory(
            package=cls.package_2,
            game=cls.game_2,
        )
        PluginGameFactory(
            plugin=cls.plugin_1,
            game=cls.game_2,
        )
        SubPluginGameFactory(
            sub_plugin=cls.sub_plugin_1,
            game=cls.game_2,
        )
        SubPluginGameFactory(
            sub_plugin=cls.sub_plugin_2,
            game=cls.game_2,
        )

        # game_3 associations
        PluginGameFactory(
            plugin=cls.plugin_2,
            game=cls.game_3,
        )

    def test_filter_backends(self):
        self.assertTupleEqual(
            tuple1=GameViewSet.filter_backends,
            tuple2=(OrderingFilter,)
        )

    def test_ordering(self):
        self.assertTupleEqual(
            tuple1=GameViewSet.ordering,
            tuple2=('name',),
        )

    def test_ordering_fields(self):
        self.assertTupleEqual(
            tuple1=GameViewSet.ordering_fields,
            tuple2=('basename', 'name', 'project_count'),
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=GameViewSet.http_method_names,
            tuple2=('get', 'options'),
        )

    def test_get_queryset(self):
        queryset = GameViewSet(action='retrieve').get_queryset().filter()
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

        queryset = GameViewSet(action='list').get_queryset().filter()
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
            expr2=getattr(PackageGame.package, 'field'),
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
            expr2=getattr(PluginGame.plugin, 'field'),
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
            expr2=getattr(SubPluginGame.sub_plugin, 'field'),
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
        request = response.wsgi_request
        icon_base_url = f'{request.scheme}://{request.get_host()}'
        self.assertDictEqual(
            d1=results[0],
            d2={
                'name': self.game_1.name,
                'slug': self.game_1.slug,
                'icon': f'{icon_base_url}{self.game_1.icon.url}',
                'package_count': 1,
                'plugin_count': 2,
                'sub_plugin_count': 0,
                'project_count': 3,
            },
        )
        self.assertDictEqual(
            d1=results[1],
            d2={
                'name': self.game_2.name,
                'slug': self.game_2.slug,
                'icon': f'{icon_base_url}{self.game_2.icon.url}',
                'package_count': 2,
                'plugin_count': 1,
                'sub_plugin_count': 2,
                'project_count': 5,
            },
        )
        self.assertDictEqual(
            d1=results[2],
            d2={
                'name': self.game_3.name,
                'slug': self.game_3.slug,
                'icon': f'{icon_base_url}{self.game_3.icon.url}',
                'package_count': 0,
                'plugin_count': 1,
                'sub_plugin_count': 0,
                'project_count': 1,
            },
        )
        self.assertDictEqual(
            d1=results[3],
            d2={
                'name': self.game_4.name,
                'slug': self.game_4.slug,
                'icon': f'{icon_base_url}{self.game_4.icon.url}',
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
                'name': self.game_2.name,
                'slug': self.game_2.slug,
                'icon': f'{icon_base_url}{self.game_2.icon.url}',
                'package_count': 2,
                'plugin_count': 1,
                'sub_plugin_count': 2,
                'project_count': 5,
            },
        )
        self.assertDictEqual(
            d1=results[1],
            d2={
                'name': self.game_1.name,
                'slug': self.game_1.slug,
                'icon': f'{icon_base_url}{self.game_1.icon.url}',
                'package_count': 1,
                'plugin_count': 2,
                'sub_plugin_count': 0,
                'project_count': 3,
            },
        )
        self.assertDictEqual(
            d1=results[2],
            d2={
                'name': self.game_3.name,
                'slug': self.game_3.slug,
                'icon': f'{icon_base_url}{self.game_3.icon.url}',
                'package_count': 0,
                'plugin_count': 1,
                'sub_plugin_count': 0,
                'project_count': 1,
            },
        )
        self.assertDictEqual(
            d1=results[3],
            d2={
                'name': self.game_4.name,
                'slug': self.game_4.slug,
                'icon': f'{icon_base_url}{self.game_4.icon.url}',
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
                viewname='api:games:games-detail',
                kwargs={'pk': self.game_1.slug},
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
        request = response.wsgi_request
        icon_base_url = f'{request.scheme}://{request.get_host()}'
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'name': self.game_1.name,
                'slug': self.game_1.slug,
                'icon': f'{icon_base_url}{self.game_1.icon.url}',
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
                viewname='api:games:games-detail',
                kwargs={'pk': self.game_2.slug},
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
                'name': self.game_2.name,
                'slug': self.game_2.slug,
                'icon': f'{icon_base_url}{self.game_2.icon.url}',
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
                viewname='api:games:games-detail',
                kwargs={'pk': self.game_3.slug},
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
                'name': self.game_3.name,
                'slug': self.game_3.slug,
                'icon': f'{icon_base_url}{self.game_3.icon.url}',
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
                viewname='api:games:games-detail',
                kwargs={'pk': self.game_4.slug},
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
                'name': self.game_4.name,
                'slug': self.game_4.slug,
                'icon': f'{icon_base_url}{self.game_4.icon.url}',
                'packages': [],
                'plugins': [],
                'sub_plugins': [],
            }
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['name'],
            second='Game List',
        )
