"""Tag API URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework import routers

# App
from project_manager.tags.api.views import TagViewSet


# =============================================================================
# >> ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'',
    viewset=TagViewSet,
    basename='tags',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
app_name = 'games'

urlpatterns = []
urlpatterns += router.urls
