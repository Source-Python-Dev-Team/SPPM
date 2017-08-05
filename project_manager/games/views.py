# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from django.views.generic import DetailView, ListView

# App
from .models import Game
from project_manager.common.helpers import get_groups


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
    model = Game
    template_name = 'games/list.html'


class GameView(DetailView):
    model = Game
    template_name = 'games/view.html'

    def get_context_data(self, **kwargs):
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
