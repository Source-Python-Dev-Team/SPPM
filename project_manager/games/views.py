"""Game views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from django.views.generic import DetailView, ListView

# App
from project_manager.common.helpers import get_groups
from project_manager.games.models import Game


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GameListView',
    'GameView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class GameListView(ListView):
    """Game listing view."""

    model = Game
    template_name = 'games/list.html'


class GameView(DetailView):
    """Game get view."""

    model = Game
    template_name = 'games/view.html'

    def get_context_data(self, **kwargs):
        """Add projects that support the current game to the context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'plugins': get_groups(self.object.plugins.all()),
            'packages': get_groups(self.object.packages.all()),
            'sub_plugins': get_groups(
                self.object.subplugins.all().select_related(
                    'plugin',
                )
            ),
        })
        return context
