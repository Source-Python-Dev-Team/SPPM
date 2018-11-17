"""Plugin API URLs."""

# =============================================================================
# >> IMPORTS
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
# >> ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'projects',
    viewset=PluginViewSet,
    base_name='projects',
)
router.register(
    prefix=r'^images/(?P<plugin_slug>[\w-]+)',
    viewset=PluginImageViewSet,
    base_name='images',
)
router.register(
    prefix=r'^releases/(?P<plugin_slug>[\w-]+)',
    viewset=PluginReleaseViewSet,
    base_name='releases',
)
router.register(
    prefix=r'^games/(?P<plugin_slug>[\w-]+)',
    viewset=PluginGameViewSet,
    base_name='games',
)
router.register(
    prefix=r'^tags/(?P<plugin_slug>[\w-]+)',
    viewset=PluginTagViewSet,
    base_name='tags',
)
router.register(
    prefix=r'^contributors/(?P<plugin_slug>[\w-]+)',
    viewset=PluginContributorViewSet,
    base_name='contributors',
)
router.register(
    prefix=r'^paths/(?P<plugin_slug>[\w-]+)',
    viewset=SubPluginPathViewSet,
    base_name='paths',
)


# =============================================================================
# >> GLOBAL VARIABLES
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
