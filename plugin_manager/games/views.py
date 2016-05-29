# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from django.views.generic import DetailView, ListView

# App
from .models import Game
from ..common.helpers import get_groups


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GameListView',
    'GameView',
)


# =============================================================================
# >> VIEW CLASSES
# =============================================================================
class GameListView(ListView):
    model = Game
    paginate_by = 20
    template_name = 'games/list.html'


class GameView(DetailView):
    model = Game
    template_name = 'games/view.html'

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        context.update({
            'plugins': get_groups(self.object.plugins.all()),
            'packages': get_groups(self.object.packages.all()),
            'sub_plugins': get_groups(self.object.sub_plugins.all()),
        })
        return context
