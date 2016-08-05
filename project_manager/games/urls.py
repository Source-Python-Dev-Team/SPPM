# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from .views import GameListView, GameView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
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
