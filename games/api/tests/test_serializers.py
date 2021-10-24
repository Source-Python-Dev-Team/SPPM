# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from rest_framework.serializers import ModelSerializer

# App
from games.api.serializers import GameSerializer
from games.models import Game


# =============================================================================
# TEST CASES
# =============================================================================
class GameSerializerTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(GameSerializer, ModelSerializer),
        )

    def test_meta_class(self):
        self.assertEqual(
            first=GameSerializer.Meta.model,
            second=Game,
        )
        self.assertTupleEqual(
            tuple1=GameSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
                'icon',
            ),
        )
