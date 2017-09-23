"""Plugin API URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# 3rd-Party Django
from rest_framework import routers

# App
from .views import (
    PluginAPIView,
    PluginImageViewSet,
    PluginReleaseViewSet,
    PluginViewSet,
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


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^$',
        view=PluginAPIView.as_view(),
        name='endpoints',
    )
]

urlpatterns += router.urls
