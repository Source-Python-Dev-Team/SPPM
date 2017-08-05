# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import include, url

# 3rd-Party Django
from rest_framework import routers

# App
from .views import SubPluginAPIView, SubPluginViewSet


# =============================================================================
# >> ROUTERS
# =============================================================================
router = routers.SimpleRouter()
# router.register(
#     prefix=r'^(?P<plugin_slug>[\w-]+)',
#     viewset=SubPluginViewSet,
#     base_name='sub-plugins'
# )
router.register(
    prefix=r'^projects/(?P<plugin_slug>[\w-]+)',
    viewset=SubPluginViewSet,
    base_name='projects'
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
