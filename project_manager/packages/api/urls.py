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
    prefix='projects',
    viewset=PackageViewSet,
    basename='projects',
)
router.register(
    prefix='images/(?P<package_slug>[^/.]+)',
    viewset=PackageImageViewSet,
    basename='images',
)
router.register(
    prefix='releases/(?P<package_slug>[^/.]+)',
    viewset=PackageReleaseViewSet,
    basename='releases',
)
router.register(
    prefix='games/(?P<package_slug>[^/.]+)',
    viewset=PackageGameViewSet,
    basename='games',
)
router.register(
    prefix='tags/(?P<package_slug>[^/.]+)',
    viewset=PackageTagViewSet,
    basename='tags',
)
router.register(
    prefix='contributors/(?P<package_slug>[^/.]+)',
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
