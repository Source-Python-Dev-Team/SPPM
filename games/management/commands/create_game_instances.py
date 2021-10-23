"""Command to create Game objects."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.management.base import BaseCommand

# App
from games.models import Game


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
GAMES = {
    'berimbau': 'Blade Symphony',
    'bms': 'Black Mesa',
    'csgo': 'Counter-Strike: Global Offensive',
    'cstrike': 'Counter-Strike: Source',
    'dod': 'Day of Defeat: Source',
    'hl2mp': 'Half-Life 2: DeathMatch',
    'left4dead2': 'Left for Dead 2',
    'tf': 'Team Fortress 2',
}


# =============================================================================
# COMMANDS
# =============================================================================
class Command(BaseCommand):
    """Populate the Game objects."""

    def handle(self, *args, **options):
        """Create any missing Game objects."""
        current_games = Game.objects.values_list('basename', flat=True)
        obj_list = []
        for game in set(GAMES).difference(current_games):
            obj_list.append(
                Game(
                    basename=game,
                    icon=f'games/{game}.png',
                    name=GAMES[game],
                    slug=game,
                )
            )

        if obj_list:  # pragma: no branch
            Game.objects.bulk_create(objs=obj_list)
