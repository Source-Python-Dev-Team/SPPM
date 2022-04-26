"""Plugin API URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import path

# Third Party Django
from rest_framework import routers

# App
from project_manager.plugins.api.views import (
    PluginAPIView,
    PluginContributorViewSet,
    PluginGameViewSet,
    PluginImageViewSet,
    PluginReleaseViewSet,
    PluginTagViewSet,
    PluginViewSet,
    SubPluginPathViewSet,
)


# =============================================================================
# ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix='projects',
    viewset=PluginViewSet,
    basename='projects',
)
router.register(
    prefix='images/(?P<plugin_slug>[^/.]+)',
    viewset=PluginImageViewSet,
    basename='images',
)
router.register(
    prefix='releases/(?P<plugin_slug>[^/.]+)',
    viewset=PluginReleaseViewSet,
    basename='releases',
)
router.register(
    prefix='games/(?P<plugin_slug>[^/.]+)',
    viewset=PluginGameViewSet,
    basename='games',
)
router.register(
    prefix='tags/(?P<plugin_slug>[^/.]+)',
    viewset=PluginTagViewSet,
    basename='tags',
)
router.register(
    prefix='contributors/(?P<plugin_slug>[^/.]+)',
    viewset=PluginContributorViewSet,
    basename='contributors',
)
router.register(
    prefix='paths/(?P<plugin_slug>[^/.]+)',
    viewset=SubPluginPathViewSet,
    basename='paths',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'plugins'

urlpatterns = [
    path(
        route='',
        view=PluginAPIView.as_view(),
        name='endpoints',
    )
]

urlpatterns += router.urls
