"""Game views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
from typing import Any

# Django
from django.views.generic import TemplateView

# App
from games.models import Game

# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    "GameView",
)


# =============================================================================
# VIEWS
# =============================================================================
class GameView(TemplateView):
    """Frontend view for viewing Games."""

    template_name = "main.html"
    http_method_names = ("get", "options")

    def get_context_data(self, **kwargs: dict) -> dict[str, Any]:
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        pk = context.get("pk")
        if pk is None:
            context["title"] = "Game Listing"
        else:
            try:
                game = Game.objects.get(pk=pk)
                context["title"] = game.name
            except Game.DoesNotExist:
                context["title"] = f'Game "{pk}" not found.'
        return context
