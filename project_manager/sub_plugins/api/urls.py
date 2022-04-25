"""SubPlugin API URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import path

# Third Party Django
from rest_framework import routers

# App
from project_manager.sub_plugins.api.views import (
    SubPluginAPIView,
    SubPluginContributorViewSet,
    SubPluginGameViewSet,
    SubPluginImageViewSet,
    SubPluginReleaseViewSet,
    SubPluginTagViewSet,
    SubPluginViewSet,
)


# =============================================================================
# ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix='projects/(?P<plugin_slug>[^/.]+)',
    viewset=SubPluginViewSet,
    basename='projects',
)
router.register(
    prefix='images/(?P<plugin_slug>[^/.]+)/(?P<sub_plugin_slug>[^/.]+)',
    viewset=SubPluginImageViewSet,
    basename='images',
)
router.register(
    prefix='releases/(?P<plugin_slug>[^/.]+)/(?P<sub_plugin_slug>[^/.]+)',
    viewset=SubPluginReleaseViewSet,
    basename='releases',
)
router.register(
    prefix='games/(?P<plugin_slug>[^/.]+)/(?P<sub_plugin_slug>[^/.]+)',
    viewset=SubPluginGameViewSet,
    basename='games',
)
router.register(
    prefix='tags/(?P<plugin_slug>[^/.]+)/(?P<sub_plugin_slug>[^/.]+)',
    viewset=SubPluginTagViewSet,
    basename='tags',
)
router.register(
    prefix=(
        'contributors/(?P<plugin_slug>[^/.]+)/(?P<sub_plugin_slug>[^/.]+)'
    ),
    viewset=SubPluginContributorViewSet,
    basename='contributors',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'sub-plugins'

urlpatterns = [
    path(
        route='',
        view=SubPluginAPIView.as_view(),
        name='endpoints',
    )
]

urlpatterns += router.urls
