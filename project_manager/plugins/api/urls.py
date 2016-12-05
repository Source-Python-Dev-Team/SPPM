# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import include, url

# 3rd-Party Django
from rest_framework import routers

# App
from .views import PluginViewSet


# =============================================================================
# >> ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'',
    viewset=PluginViewSet,
    base_name='plugins'
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^',
        view=include(router.urls),
    )
]
