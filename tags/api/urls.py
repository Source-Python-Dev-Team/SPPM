"""Tag API URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework import routers

# App
from tags.api.views import TagViewSet


# =============================================================================
# ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix='',
    viewset=TagViewSet,
    basename='tags',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'games'

urlpatterns = []
urlpatterns += router.urls
