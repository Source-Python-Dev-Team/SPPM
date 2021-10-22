"""Plugin API URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# 3rd-Party Django
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
    prefix=r'projects',
    viewset=PluginViewSet,
    basename='projects',
)
router.register(
    prefix=r'^images/(?P<plugin_slug>[\w-]+)',
    viewset=PluginImageViewSet,
    basename='images',
)
router.register(
    prefix=r'^releases/(?P<plugin_slug>[\w-]+)',
    viewset=PluginReleaseViewSet,
    basename='releases',
)
router.register(
    prefix=r'^games/(?P<plugin_slug>[\w-]+)',
    viewset=PluginGameViewSet,
    basename='games',
)
router.register(
    prefix=r'^tags/(?P<plugin_slug>[\w-]+)',
    viewset=PluginTagViewSet,
    basename='tags',
)
router.register(
    prefix=r'^contributors/(?P<plugin_slug>[\w-]+)',
    viewset=PluginContributorViewSet,
    basename='contributors',
)
router.register(
    prefix=r'^paths/(?P<plugin_slug>[\w-]+)',
    viewset=SubPluginPathViewSet,
    basename='paths',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'plugins'

urlpatterns = [
    url(
        regex=r'^$',
        view=PluginAPIView.as_view(),
        name='endpoints',
    )
]

urlpatterns += router.urls
