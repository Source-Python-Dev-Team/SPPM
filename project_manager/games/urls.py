"""Game URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from project_manager.games.views import GameListView, GameView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
app_name = 'games'

urlpatterns = [
    url(
        # /games/
        regex=r'^$',
        view=GameListView.as_view(),
        name='list',
    ),
    url(
        # /games/<slug>/
        regex=r'^(?P<slug>[\w-]+)/$',
        view=GameView.as_view(),
        name='detail',
    ),
]
