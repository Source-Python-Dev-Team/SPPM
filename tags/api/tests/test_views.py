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
class TagViewSetAPITestCase(APITestCase):

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

    def test_can_list(self):
        response = self.client.get(path='/api/tags/')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=0,
        )

        tag = TagFactory()
        response = self.client.get(path='/api/tags/')
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

    def test_cannot_post(self):
        response = self.client.post(
            path='/api/tags/',
            data={
                'name': 'test',
            }
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
