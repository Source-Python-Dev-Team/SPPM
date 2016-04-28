# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.conf.urls import url

# App Imports
from .views import GameListView, GameView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^$',
        view=GameListView.as_view(),
        name='list',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=GameView.as_view(),
        name='detail',
    ),
]
