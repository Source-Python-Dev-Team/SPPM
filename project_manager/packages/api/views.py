"""Package API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.helpers import get_prefetch
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectImageViewSet,
    ProjectViewSet,
)
from .filters import PackageFilter
from .serializers import PackageImageSerializer, PackageSerializer
from ..models import Package, PackageImage, PackageRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAPIView',
    'PackageImageViewSet',
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
            image_class=PackageImage,
        )
    ).select_related(
        'owner__user',
    )
    serializer_class = PackageSerializer


class PackageImageViewSet(ProjectImageViewSet):
    """ViewSet for adding, removing, and listing images for Packages."""

    queryset = PackageImage.objects.select_related(
        'package',
    )
    serializer_class = PackageImageSerializer

    project_type = 'package'
    project_model = Package
