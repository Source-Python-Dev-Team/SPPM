# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase
from django.urls import reverse
from django.views.generic import TemplateView

# Third Party Django
from rest_framework import status

# App
from games.views import GameView
from test_utils.factories.games import GameFactory


# =============================================================================
# TEST CASES
# =============================================================================
class GameViewTestCase(TestCase):

    def test_view_inheritance(self):
        self.assertTrue(
            expr=issubclass(GameView, TemplateView),
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=GameView.http_method_names,
            tuple2=("get", "options"),
        )

    def test_template_name(self):
        self.assertEqual(
            first=GameView.template_name,
            second="main.html",
        )

    def test_get_list(self):
        response = self.client.get(
            path=reverse(
                viewname="games:list",
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data["view"]
        self.assertDictEqual(
            d1=data,
            d2={"title": "Game Listing"},
        )

    def test_get_detail(self):
        game = GameFactory()
        response = self.client.get(
            path=reverse(
                viewname="games:detail",
                kwargs={
                    "pk": game.pk,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data["view"]
        self.assertDictEqual(
            d1=data,
            d2={
                "pk": str(game.pk),
                "title": game.name,
            },
        )

    def test_detail_invalid_slug(self):
        response = self.client.get(
            path=reverse(
                viewname="games:detail",
                kwargs={
                    "pk": 1,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data["view"]
        self.assertDictEqual(
            d1=data,
            d2={
                "pk": "1",
                "title": 'Game "1" not found.',
            },
        )
