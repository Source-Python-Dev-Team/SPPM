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
from project_manager.packages.api.serializers.common import (
    ReleasePackageRequirementSerializer,
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
from project_manager.requirements.api.serializers.common import (
    ReleaseDownloadRequirementSerializer,
    ReleasePyPiRequirementSerializer,
    ReleaseVersionControlRequirementSerializer,
)
from .mixins import PackageReleaseBase


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageContributorSerializer',
    'PackageCreateReleaseSerializer',
    'PackageCreateSerializer',
    'PackageGameSerializer',
    'PackageImageSerializer',
    'PackageReleaseSerializer',
    'PackageSerializer',
    'PackageTagSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class PackageImageSerializer(ProjectImageSerializer):
    """Serializer for adding, removing, and listing Package images."""

    class Meta(ProjectImageSerializer.Meta):
        model = PackageImage


class PackageReleasePackageRequirementSerializer(
    ReleasePackageRequirementSerializer
):
    """Serializer for Package Release Package requirements."""

    class Meta(ReleasePackageRequirementSerializer.Meta):
        model = PackageReleasePackageRequirement


class PackageReleaseDownloadRequirementSerializer(
    ReleaseDownloadRequirementSerializer
):
    """Serializer for Package Release Download requirements."""

    class Meta(ReleaseDownloadRequirementSerializer.Meta):
        model = PackageReleaseDownloadRequirement


class PackageReleasePyPiRequirementSerializer(
    ReleasePyPiRequirementSerializer
):
    """Serializer for Package Release PyPi requirements."""

    class Meta(ReleasePyPiRequirementSerializer.Meta):
        model = PackageReleasePyPiRequirement


class PackageReleaseVersionControlRequirementSerializer(
    ReleaseVersionControlRequirementSerializer
):
    """Serializer for Package Release VCS requirements."""

    class Meta(ReleaseVersionControlRequirementSerializer.Meta):
        model = PackageReleaseVersionControlRequirement


class PackageReleaseSerializer(PackageReleaseBase, ProjectReleaseSerializer):
    """Serializer for listing Package releases."""

    download_requirements = PackageReleaseDownloadRequirementSerializer(
        source='packagereleasedownloadrequirement_set',
        read_only=True,
        many=True,
    )
    package_requirements = PackageReleasePackageRequirementSerializer(
        source='packagereleasepackagerequirement_set',
        read_only=True,
        many=True,
    )
    pypi_requirements = PackageReleasePyPiRequirementSerializer(
        source='packagereleasepypirequirement_set',
        read_only=True,
        many=True,
    )
    vcs_requirements = PackageReleaseVersionControlRequirementSerializer(
        source='packagereleaseversioncontrolrequirement_set',
        read_only=True,
        many=True,
    )

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
    """Supported Games Serializer for Packages."""

    class Meta(ProjectGameSerializer.Meta):
        model = PackageGame


class PackageTagSerializer(ProjectTagSerializer):
    """Tags Serializer for Packages."""

    class Meta(ProjectTagSerializer.Meta):
        model = PackageTag


class PackageContributorSerializer(ProjectContributorSerializer):
    """Contributors Serializer for Packages."""

    class Meta(ProjectContributorSerializer.Meta):
        model = PackageContributor
