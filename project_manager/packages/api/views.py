"""Package API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.helpers import get_prefetch
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectReleaseViewSet,
    ProjectTagViewSet,
    ProjectViewSet,
)
from .filters import PackageFilter
from .serializers import (
    PackageContributorSerializer,
    PackageCreateSerializer,
    PackageGameSerializer,
    PackageImageSerializer,
    PackageReleaseSerializer,
    PackageSerializer,
    PackageTagSerializer,
)
from ..models import (
    Package,
    PackageContributor,
    PackageGame,
    PackageImage,
    PackageRelease,
    PackageTag,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAPIView',
    'PackageContributorsViewSet',
    'PackageGameViewSet',
    'PackageImageViewSet',
    'PackageReleaseViewSet',
    'PackageTagViewSet',
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


class PackageGameViewSet(ProjectGameViewSet):
    """Supported Games listing for Packages."""

    queryset = PackageGame.objects.select_related(
        'game',
        'package',
    )
    serializer_class = PackageGameSerializer

    project_type = 'package'
    project_model = Package


class PackageTagViewSet(ProjectTagViewSet):
    """Tags listing for Packages."""

    queryset = PackageTag.objects.select_related(
        'tag',
        'package',
    )
    serializer_class = PackageTagSerializer

    project_type = 'package'
    project_model = Package


class PackageContributorsViewSet(ProjectContributorViewSet):
    """Contributors listing for Packages."""

    queryset = PackageContributor.objects.select_related(
        'user__user',
        'package',
    )
    serializer_class = PackageContributorSerializer

    project_type = 'package'
    project_model = Package
