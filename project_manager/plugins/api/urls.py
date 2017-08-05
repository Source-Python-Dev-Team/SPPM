# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# 3rd-Party Django
from rest_framework import routers

# App
from .views import PluginAPIView, PluginViewSet


# =============================================================================
# >> ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'projects',
    viewset=PluginViewSet,
    base_name='projects'
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^$',
        view=PluginAPIView.as_view(),
        name='endpoints'
    )
]

urlpatterns += router.urls
