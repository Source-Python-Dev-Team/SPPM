# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from django.views.generic import DetailView, ListView

# App Imports
from .models import Game


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GameListView',
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
            'plugins': self.get_groups(self.object.plugins.all()),
            'packages': self.get_groups(self.object.packages.all()),
            'sub_plugins': self.get_groups(self.object.sub_plugins.all()),
        })
        return context

    @staticmethod
    def get_groups(iterable, n=3):
        if not iterable:
            return iterable
        iterable = list(iterable)
        remainder = len(iterable) % n
        iterable.extend([''] * (n - remainder))
        return zip(*(iter(iterable), ) * n)
