"""Package API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db.models import Prefetch

# App
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
    """ViewSet for creating, updating, and listing Packages.

    ###Available Filters:
    *  **game**=*{game}*
        * Filters on supported games with exact match to slug.

        ####Example:
        `?game=csgo`

        `?game=cstrike`

    *  **tag**=*{tag}*
        * Filters on tags using exact match.

        ####Example:
        `?tag=wcs`

        `?tag=sounds`

    *  **user**=*{username}*
        * Filters on username using exact match with owner/contributors.

        ####Example:
        `?user=satoon101`

        `?user=Ayuto`

    ###Available Ordering:

    *  **name** (descending) or **-name** (ascending)
    *  **basename** (descending) or **-basename** (ascending)
    *  **updated** (descending) or **-updated** (ascending)

        ####Example:
        `?ordering=basename`

        `?ordering=-updated`
    """

    filter_class = PackageFilter
    queryset = Package.objects.prefetch_related(
        Prefetch(
            lookup='releases',
            queryset=PackageRelease.objects.order_by(
                '-created',
            ),
        ),
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
