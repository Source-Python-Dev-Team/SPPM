"""Factories for use when testing with Game functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
import factory

# App
from games.models import Game


# =============================================================================
# FACTORIES
# =============================================================================
class GameFactory(factory.django.DjangoModelFactory):
    """Model factory to use when testing with Game objects."""

    class Meta:
        """Define metaclass attributes."""
        model = Game
