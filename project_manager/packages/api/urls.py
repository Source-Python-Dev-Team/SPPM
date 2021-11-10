"""Package API URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import path

# Third Party Django
from rest_framework import routers

# App
from project_manager.packages.api.views import (
    PackageAPIView,
    PackageContributorViewSet,
    PackageGameViewSet,
    PackageImageViewSet,
    PackageReleaseViewSet,
    PackageTagViewSet,
    PackageViewSet,
)


# =============================================================================
# ROUTERS
# =============================================================================
router = routers.SimpleRouter()
router.register(
    prefix=r'projects',
    viewset=PackageViewSet,
    basename='projects',
)
router.register(
    prefix=r'^images/(?P<package_slug>[\w-]+)',
    viewset=PackageImageViewSet,
    basename='images',
)
router.register(
    prefix=r'^releases/(?P<package_slug>[\w-]+)',
    viewset=PackageReleaseViewSet,
    basename='releases',
)
router.register(
    prefix=r'^games/(?P<package_slug>[\w-]+)',
    viewset=PackageGameViewSet,
    basename='games',
)
router.register(
    prefix=r'^tags/(?P<package_slug>[\w-]+)',
    viewset=PackageTagViewSet,
    basename='tags',
)
router.register(
    prefix=r'^contributors/(?P<package_slug>[\w-]+)',
    viewset=PackageContributorViewSet,
    basename='contributors',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'packages'

urlpatterns = [
    path(
        route='',
        view=PackageAPIView.as_view(),
        name='endpoints',
    )
]

urlpatterns += router.urls
