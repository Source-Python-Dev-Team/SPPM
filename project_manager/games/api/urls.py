"""Game API URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework import routers

# App
from project_manager.games.api.views import GameViewSet


# =============================================================================
# >> ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'',
    viewset=GameViewSet,
    basename='games',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
app_name = 'games'

urlpatterns = []
urlpatterns += router.urls
