# =============================================================================
# IMPORTS
# =============================================================================
# Python
from random import choice

# Django
from django.core.management import call_command
from django.test import TestCase

# App
from games.management.commands.create_game_instances import GAMES
from games.models import Game
from test_utils.factories.games import GameFactory


# =============================================================================
# TEST CASES
# =============================================================================
class CommandsTestCase(TestCase):
    def test_create_game_instances(self):
        game = choice(list(GAMES))
        GameFactory(
            name=GAMES[game],
            basename=game,
            icon=f'games/{game}.png',
        )
        self.assertEqual(
            first=Game.objects.count(),
            second=1,
        )
        call_command('create_game_instances')
        self.assertEqual(
            first=Game.objects.count(),
            second=len(GAMES),
        )
