"""Package serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.serializers import (
    ProjectImageSerializer,
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
    """Serializer for creating, updating, and listing Packages."""

    images = PackageImageSerializer(
        many=True,
        read_only=True,
    )
    releases = PackageReleaseSerializer(
        write_only=True,
    )

    project_type = 'package'
    release_model = PackageRelease

    class Meta(ProjectSerializer.Meta):
        model = Package
        fields = ProjectSerializer.Meta.fields + (
            'images',
            'releases',
        )
