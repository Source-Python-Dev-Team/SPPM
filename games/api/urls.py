"""Game API URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework import routers

# App
from games.api.views import GameViewSet


# =============================================================================
# ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix='',
    viewset=GameViewSet,
    basename='games',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'games'

urlpatterns = []
urlpatterns += router.urls
