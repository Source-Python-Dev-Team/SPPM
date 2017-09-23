"""SubPlugin API URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# 3rd-Party Django
from rest_framework import routers

# App
from .views import (
    SubPluginAPIView,
    SubPluginImageViewSet,
    SubPluginReleaseViewSet,
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


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^$',
        view=SubPluginAPIView.as_view(),
        name='endpoints',
    )
]

urlpatterns += router.urls
