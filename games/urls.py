"""Game URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import path

# App
from games.views import GameView

# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = "games"

urlpatterns = [
    path(
        # /games
        route="",
        view=GameView.as_view(),
        name="list",
    ),
    path(
        # /games/<pk>
        route="<pk>/",
        view=GameView.as_view(),
        name="detail",
    ),
]
