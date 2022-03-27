"""Factories for use when testing with Game functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
import factory

# App
from games.models import Game


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'GameFactory',
)


# =============================================================================
# FACTORIES
# =============================================================================
class GameFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with Game objects."""

    name = factory.Sequence(function=lambda n: f'Game {n}')
    basename = factory.Sequence(function=lambda n: f'game_{n}')
    icon = factory.Sequence(function=lambda n: f'game_{n}.png')

    class Meta:
        """Define metaclass attributes."""

        model = Game
