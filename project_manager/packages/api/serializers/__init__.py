"""Package serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.serializers import (
    ProjectImageSerializer,
    ProjectReleaseSerializer,
    ProjectCreateReleaseSerializer,
    ProjectSerializer,
)
from project_manager.packages.models import (
    Package,
    PackageImage,
    PackageRelease,
)
from ..mixins import PackageReleaseBase


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageImageSerializer',
    'PackageCreateReleaseSerializer',
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
