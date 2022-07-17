"""Package API views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Prefetch

# App
from project_manager.api.common.views import (
    ProjectAPIView,
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectReleaseViewSet,
    ProjectTagViewSet,
    ProjectViewSet,
)
from project_manager.packages.api.filtersets import PackageFilterSet
from project_manager.packages.api.serializers import (
    PackageContributorSerializer,
    PackageCreateSerializer,
    PackageGameSerializer,
    PackageImageSerializer,
    PackageReleaseSerializer,
    PackageSerializer,
    PackageTagSerializer,
)
from project_manager.packages.models import (
    Package,
    PackageContributor,
    PackageGame,
    PackageImage,
    PackageRelease,
    PackageReleaseDownloadRequirement,
    PackageReleasePackageRequirement,
    PackageReleasePyPiRequirement,
    PackageReleaseVersionControlRequirement,
    PackageTag,
)
from users.models import ForumUser


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAPIView',
    'PackageContributorViewSet',
    'PackageGameViewSet',
    'PackageImageViewSet',
    'PackageReleaseViewSet',
    'PackageTagViewSet',
    'PackageViewSet',
)


# =============================================================================
# VIEWS
# =============================================================================
class PackageAPIView(ProjectAPIView):
    """Package API routes."""

    project_type = 'package'


class PackageViewSet(ProjectViewSet):
    """ViewSet for creating, updating, and listing Packages."""

    __doc__ += ProjectViewSet.doc_string
    filterset_class = PackageFilterSet
    queryset = Package.objects.select_related(
        'owner__user',
    ).prefetch_related(
        Prefetch(
            lookup='releases',
            queryset=PackageRelease.objects.order_by(
                '-created',
            ),
        ),
        Prefetch(
            lookup='contributors',
            queryset=ForumUser.objects.select_related('user'),
        ),
    )
    serializer_class = PackageSerializer

    creation_serializer_class = PackageCreateSerializer


class PackageImageViewSet(ProjectImageViewSet):
    """ViewSet for adding, removing, and listing images for Packages."""

    __doc__ += ProjectImageViewSet.doc_string
    queryset = PackageImage.objects.select_related(
        'package',
    )
    serializer_class = PackageImageSerializer

    project_type = 'package'
    project_model = Package


class PackageReleaseViewSet(ProjectReleaseViewSet):
    """ViewSet for retrieving releases for Packages."""

    __doc__ += ProjectReleaseViewSet.doc_string
    queryset = PackageRelease.objects.select_related(
        'package',
        'created_by__user',
    ).prefetch_related(
        Prefetch(
            lookup='packagereleasepackagerequirement_set',
            queryset=PackageReleasePackageRequirement.objects.order_by(
                'package_requirement__name',
            ).select_related(
                'package_requirement',
            )
        ),
        Prefetch(
            lookup='packagereleasedownloadrequirement_set',
            queryset=PackageReleaseDownloadRequirement.objects.order_by(
                'download_requirement__url',
            ).select_related(
                'download_requirement',
            )
        ),
        Prefetch(
            lookup='packagereleasepypirequirement_set',
            queryset=PackageReleasePyPiRequirement.objects.order_by(
                'pypi_requirement__name',
            ).select_related(
                'pypi_requirement',
            )
        ),
        Prefetch(
            lookup='packagereleaseversioncontrolrequirement_set',
            queryset=PackageReleaseVersionControlRequirement.objects.order_by(
                'vcs_requirement__url',
            ).select_related(
                'vcs_requirement',
            )
        ),
    )
    serializer_class = PackageReleaseSerializer

    project_type = 'package'
    project_model = Package


class PackageGameViewSet(ProjectGameViewSet):
    """Supported Games listing for Packages."""

    __doc__ += ProjectGameViewSet.doc_string
    queryset = PackageGame.objects.select_related(
        'game',
        'package',
    )
    serializer_class = PackageGameSerializer

    project_type = 'package'
    project_model = Package


class PackageTagViewSet(ProjectTagViewSet):
    """Tags listing for Packages."""

    __doc__ += ProjectTagViewSet.doc_string
    queryset = PackageTag.objects.select_related(
        'tag',
        'package',
    )
    serializer_class = PackageTagSerializer

    project_type = 'package'
    project_model = Package


class PackageContributorViewSet(ProjectContributorViewSet):
    """Contributors listing for Packages."""

    __doc__ += ProjectContributorViewSet.doc_string
    queryset = PackageContributor.objects.select_related(
        'user__user',
        'package',
    )
    serializer_class = PackageContributorSerializer

    project_type = 'package'
    project_model = Package
