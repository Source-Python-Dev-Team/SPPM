"""SubPlugin API URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# 3rd-Party Django
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
# >> ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'^projects/(?P<plugin_slug>[\w-]+)',
    viewset=SubPluginViewSet,
    base_name='projects',
)
router.register(
    prefix=r'^images/(?P<plugin_slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)',
    viewset=SubPluginImageViewSet,
    base_name='images',
)
router.register(
    prefix=r'^releases/(?P<plugin_slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)',
    viewset=SubPluginReleaseViewSet,
    base_name='releases',
)
router.register(
    prefix=r'^games/(?P<plugin_slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)',
    viewset=SubPluginGameViewSet,
    base_name='games',
)
router.register(
    prefix=r'^tags/(?P<plugin_slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)',
    viewset=SubPluginTagViewSet,
    base_name='tags',
)
router.register(
    prefix=(
        r'^contributors/(?P<plugin_slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)'
    ),
    viewset=SubPluginContributorViewSet,
    base_name='contributors',
)


# =============================================================================
# >> GLOBAL VARIABLES
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
