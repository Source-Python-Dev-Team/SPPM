"""Package API URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# 3rd-Party Django
from rest_framework import routers

# App
from .views import (
    PackageAPIView,
    PackageContributorsViewSet,
    PackageGameViewSet,
    PackageImageViewSet,
    PackageReleaseViewSet,
    PackageTagViewSet,
    PackageViewSet,
)


# =============================================================================
# >> ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'projects',
    viewset=PackageViewSet,
    base_name='projects',
)
router.register(
    prefix=r'^images/(?P<package_slug>[\w-]+)',
    viewset=PackageImageViewSet,
    base_name='images',
)
router.register(
    prefix=r'^releases/(?P<package_slug>[\w-]+)',
    viewset=PackageReleaseViewSet,
    base_name='releases',
)
router.register(
    prefix=r'^games/(?P<package_slug>[\w-]+)',
    viewset=PackageGameViewSet,
    base_name='games',
)
router.register(
    prefix=r'^tags/(?P<package_slug>[\w-]+)',
    viewset=PackageTagViewSet,
    base_name='tags',
)
router.register(
    prefix=r'^contributors/(?P<package_slug>[\w-]+)',
    viewset=PackageContributorsViewSet,
    base_name='contributors',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
app_name = 'packages'

urlpatterns = [
    url(
        regex=r'^$',
        view=PackageAPIView.as_view(),
        name='endpoints',
    )
]

urlpatterns += router.urls
