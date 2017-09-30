"""Package serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.serializers import (
    ProjectContributorSerializer,
    ProjectCreateReleaseSerializer,
    ProjectGameSerializer,
    ProjectImageSerializer,
    ProjectReleaseSerializer,
    ProjectSerializer,
    ProjectTagSerializer,
)
from project_manager.packages.models import (
    Package,
    PackageContributor,
    PackageGame,
    PackageImage,
    PackageRelease,
    PackageTag,
)
from ..mixins import PackageReleaseBase


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageCreateSerializer',
    'PackageCreateReleaseSerializer',
    'PackageImageSerializer',
    'PackageReleaseSerializer',
    'PackageSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class PackageImageSerializer(ProjectImageSerializer):
    """Serializer for adding, removing, and listing Package images."""

    class Meta(ProjectImageSerializer.Meta):
        model = PackageImage


class PackageReleaseSerializer(PackageReleaseBase, ProjectReleaseSerializer):
    """Serializer for listing Package releases."""

    class Meta(ProjectReleaseSerializer.Meta):
        model = PackageRelease


class PackageCreateReleaseSerializer(
    PackageReleaseBase, ProjectCreateReleaseSerializer
):
    """Serializer for creating and listing Package releases."""

    class Meta(ProjectCreateReleaseSerializer.Meta):
        model = PackageRelease


class PackageSerializer(ProjectSerializer):
    """Serializer for updating and listing Packages."""

    project_type = 'package'
    release_model = PackageRelease

    class Meta(ProjectSerializer.Meta):
        model = Package


class PackageCreateSerializer(PackageSerializer):
    """Serializer for creating Packages."""

    releases = PackageCreateReleaseSerializer(
        write_only=True,
    )

    class Meta(PackageSerializer.Meta):
        fields = PackageSerializer.Meta.fields + (
            'releases',
        )


class PackageGameSerializer(ProjectGameSerializer):
    """"""

    class Meta(ProjectGameSerializer.Meta):
        model = PackageGame


class PackageTagSerializer(ProjectTagSerializer):
    """"""

    class Meta(ProjectTagSerializer.Meta):
        model = PackageTag


class PackageContributorSerializer(ProjectContributorSerializer):
    """"""

    class Meta(ProjectContributorSerializer.Meta):
        model = PackageContributor
