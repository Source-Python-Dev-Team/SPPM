"""Game app config."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.apps import AppConfig


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'GameConfig',
)


# =============================================================================
# APPLICATION CONFIG
# =============================================================================
class GameConfig(AppConfig):
    """Game app config."""

    name = 'games'
    verbose_name = 'Games'