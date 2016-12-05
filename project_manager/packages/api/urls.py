# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import include, url

# 3rd-Party Django
from rest_framework import routers

# App
from .views import PackageViewSet


# =============================================================================
# >> ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'',
    viewset=PackageViewSet,
    base_name='packages'
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
