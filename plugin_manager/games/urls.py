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
        # http://plugins.sourcepython.com/games/
        regex=r'^$',
        view=GameListView.as_view(),
        name='list',
    ),
    url(
        # http://plugins.sourcepython.com/games/<slug>/
        regex=r'^(?P<slug>[\w-]+)/$',
        view=GameView.as_view(),
        name='detail',
    ),
]
