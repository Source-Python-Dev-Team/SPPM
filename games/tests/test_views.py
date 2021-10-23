from django.core.management import call_command

from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.test import APITestCase

from games.api.serializers import GameSerializer
from games.api.views import GameViewSet
from games.management.commands.create_game_instances import GAMES


class GameViewSetAPITestCase(APITestCase):

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

    def test_can_list(self):
        response = self.client.get(path='/api/games/')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=0,
        )

        call_command('create_game_instances')
        response = self.client.get(path='/api/games/')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=len(GAMES),
        )

    def test_cannot_post(self):
        game = list(GAMES)[0]
        response = self.client.post(
            path='/api/games/',
            data={
                'basename': game,
                'icon': f'games/{game}.png',
                'name': GAMES[game],
            }
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
