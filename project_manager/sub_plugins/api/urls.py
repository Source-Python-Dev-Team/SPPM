"""SubPlugin API URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

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
    prefix=r'^projects/(?P<plugin_slug>[\w-]+)',
    viewset=SubPluginViewSet,
    basename='projects',
)
router.register(
    prefix=r'^images/(?P<plugin_slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)',
    viewset=SubPluginImageViewSet,
    basename='images',
)
router.register(
    prefix=r'^releases/(?P<plugin_slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)',
    viewset=SubPluginReleaseViewSet,
    basename='releases',
)
router.register(
    prefix=r'^games/(?P<plugin_slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)',
    viewset=SubPluginGameViewSet,
    basename='games',
)
router.register(
    prefix=r'^tags/(?P<plugin_slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)',
    viewset=SubPluginTagViewSet,
    basename='tags',
)
router.register(
    prefix=(
        r'^contributors/(?P<plugin_slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)'
    ),
    viewset=SubPluginContributorViewSet,
    basename='contributors',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'sub-plugins'

urlpatterns = [
    url(
        regex=r'^$',
        view=SubPluginAPIView.as_view(),
        name='endpoints',
    )
]

urlpatterns += router.urls
