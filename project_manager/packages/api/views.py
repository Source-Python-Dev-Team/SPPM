"""Package API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.helpers import get_prefetch
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectImageViewSet,
    ProjectReleaseViewSet,
    ProjectViewSet,
)
from .filters import PackageFilter
from .serializers import (
    PackageCreateSerializer,
    PackageImageSerializer,
    PackageReleaseSerializer,
    PackageSerializer,
)
from ..models import Package, PackageImage, PackageRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAPIView',
    'PackageImageViewSet',
    'PackageReleaseViewSet',
    'PackageViewSet',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PackageAPIView(ProjectAPIView):
    """Package API routes."""

    project_type = 'package'


class PackageViewSet(ProjectViewSet):
    """ViewSet for creating, updating, and listing Packages."""

    filter_class = PackageFilter
    queryset = Package.objects.prefetch_related(
        *get_prefetch(
            release_class=PackageRelease,
        )
    ).select_related(
        'owner__user',
    )
    serializer_class = PackageSerializer

    creation_serializer_class = PackageCreateSerializer


class PackageImageViewSet(ProjectImageViewSet):
    """ViewSet for adding, removing, and listing images for Packages."""

    queryset = PackageImage.objects.select_related(
        'package',
    )
    serializer_class = PackageImageSerializer

    project_type = 'package'
    project_model = Package


class PackageReleaseViewSet(ProjectReleaseViewSet):
    """ViewSet for retrieving releases for Packages."""

    queryset = PackageRelease.objects.select_related(
        'package',
    )
    serializer_class = PackageReleaseSerializer

    project_type = 'package'
    project_model = Package
