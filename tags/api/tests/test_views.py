# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.test import APITestCase

# App
from tags.api.serializers import TagSerializer
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

    api_path = '/api/tags/'

    def test_filter_backends(self):
        self.assertTupleEqual(
            tuple1=TagViewSet.filter_backends,
            tuple2=(OrderingFilter, DjangoFilterBackend)
        )

    def test_serializer_class(self):
        self.assertEqual(
            first=TagViewSet.serializer_class,
            second=TagSerializer,
        )

    def test_ordering(self):
        self.assertTupleEqual(
            tuple1=TagViewSet.ordering,
            tuple2=('name',),
        )

    def test_ordering_fields(self):
        self.assertTupleEqual(
            tuple1=TagViewSet.ordering_fields,
            tuple2=('name',),
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=TagViewSet.http_method_names,
            tuple2=('get', 'options'),
        )

    def test_get_queryset(self):
        queryset = TagViewSet().get_queryset().filter()
        prefetch_lookups = queryset._prefetch_related_lookups
        self.assertEqual(
            first=len(prefetch_lookups),
            second=3,
        )
        for n, lookup_name in enumerate([
            'packages',
            'plugins',
            'subplugins',
        ]):
            lookup = prefetch_lookups[n]
            self.assertEqual(
                first=lookup.prefetch_to,
                second=lookup_name,
            )
            self.assertEqual(
                first=lookup.queryset.query.order_by,
                second=('name',),
            )

        self.assertDictEqual(
            d1=queryset.query.select_related,
            d2={'creator': {'user': {}}},
        )

    def test_get(self):
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=0,
        )

        tag_1 = TagFactory()
        package = PackageFactory()
        PackageTagFactory(
            package=package,
            tag=tag_1,
        )
        tag_2 = TagFactory()
        plugin = PluginFactory()
        PluginTagFactory(
            plugin=plugin,
            tag=tag_2,
        )
        tag_3 = TagFactory()
        sub_plugin = SubPluginFactory(
            plugin=plugin,
        )
        SubPluginTagFactory(
            sub_plugin=sub_plugin,
            tag=tag_3,
        )
        tag_4 = TagFactory()
        black_listed_tag = TagFactory(
            black_listed=True,
        )
        response = self.client.get(path=self.api_path)
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
                'name': tag_1.name,
                'packages': [package.name],
                'plugins': [],
                'subplugins': [],
                'creator': {
                    'forum_id': tag_1.creator.forum_id,
                    'username': tag_1.creator.user.username,
                }
            }
        )
        self.assertDictEqual(
            d1=results[1],
            d2={
                'name': tag_2.name,
                'packages': [],
                'plugins': [plugin.name],
                'subplugins': [],
                'creator': {
                    'forum_id': tag_2.creator.forum_id,
                    'username': tag_2.creator.user.username,
                }
            }
        )
        self.assertDictEqual(
            d1=results[2],
            d2={
                'name': tag_3.name,
                'packages': [],
                'plugins': [],
                'subplugins': [sub_plugin.name],
                'creator': {
                    'forum_id': tag_3.creator.forum_id,
                    'username': tag_3.creator.user.username,
                }
            }
        )
        self.assertDictEqual(
            d1=results[3],
            d2={
                'name': tag_4.name,
                'packages': [],
                'plugins': [],
                'subplugins': [],
                'creator': {
                    'forum_id': tag_4.creator.forum_id,
                    'username': tag_4.creator.user.username,
                }
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
            second='Tag List',
        )
