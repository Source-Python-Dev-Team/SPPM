"""Package serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.serializers import (
    ProjectImageSerializer,
    ProjectReleaseListSerializer,
    ProjectReleaseSerializer,
    ProjectSerializer,
)
from project_manager.packages.helpers import get_package_basename
from project_manager.packages.models import (
    Package,
    PackageImage,
    PackageRelease,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
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


class PackageReleaseListSerializer(ProjectReleaseListSerializer):
    """Serializer for listing Package releases."""

    class Meta(ProjectReleaseListSerializer.Meta):
        model = PackageRelease


class PackageReleaseSerializer(ProjectReleaseSerializer):
    """Serializer for creating and listing Package releases."""

    project_class = Package
    project_type = 'package'

    class Meta(ProjectReleaseSerializer.Meta):
        model = PackageRelease

    @property
    def zip_parser(self):
        return get_package_basename


class PackageSerializer(ProjectSerializer):
    """Serializer for updating and listing Packages."""

    project_type = 'package'
    release_model = PackageRelease

    class Meta(ProjectSerializer.Meta):
        model = Package


class PackageCreateSerializer(PackageSerializer):
    """Serializer for creating Packages."""

    releases = PackageReleaseSerializer(
        write_only=True,
    )

    class Meta(PackageSerializer.Meta):
        fields = PackageSerializer.Meta.fields + (
            'releases',
        )
