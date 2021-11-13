# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.management import call_command

# Third Party Django
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.test import APITestCase

# App
from games.api.serializers import GameSerializer
from games.api.views import GameViewSet
from games.management.commands.create_game_instances import GAMES


# =============================================================================
# TEST CASES
# =============================================================================
class GameViewSetTestCase(APITestCase):

    api_path = '/api/games/'

    def test_filter_backends(self):
        self.assertTupleEqual(
            tuple1=GameViewSet.filter_backends,
            tuple2=(OrderingFilter,)
        )

    def test_serializer_class(self):
        self.assertEqual(
            first=GameViewSet.serializer_class,
            second=GameSerializer,
        )

    def test_ordering(self):
        self.assertTupleEqual(
            tuple1=GameViewSet.ordering,
            tuple2=('name',),
        )

    def test_ordering_fields(self):
        self.assertTupleEqual(
            tuple1=GameViewSet.ordering_fields,
            tuple2=('basename', 'name',),
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=GameViewSet.http_method_names,
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

        call_command('create_game_instances')
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=len(GAMES),
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
