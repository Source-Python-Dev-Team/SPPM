# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.test import APITestCase

# App
from tags.api.filtersets import TagFilterSet
from tags.api.serializers import TagSerializer
from tags.api.views import TagViewSet
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

    def test_filterset_class(self):
        self.assertEqual(
            first=TagViewSet.filterset_class,
            second=TagFilterSet,
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

        tag = TagFactory()
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=1,
        )
        self.assertEqual(
            first=content['results'][0]['name'],
            second=tag.name,
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
