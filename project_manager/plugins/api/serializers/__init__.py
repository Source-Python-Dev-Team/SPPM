"""Plugin serializers for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.exceptions import ValidationError

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
from project_manager.common.api.serializers.mixins import ProjectThroughMixin
from project_manager.packages.api.serializers.common import (
    ReleasePackageRequirementSerializer,
)
from project_manager.plugins.api.serializers.mixins import PluginReleaseBase
from project_manager.plugins.models import (
    Plugin,
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginRelease,
    PluginReleaseDownloadRequirement,
    PluginReleasePackageRequirement,
    PluginReleasePyPiRequirement,
    PluginReleaseVersionControlRequirement,
    PluginTag,
    SubPluginPath,
)
from requirements.api.serializers.common import (
    ReleaseDownloadRequirementSerializer,
    ReleasePyPiRequirementSerializer,
    ReleaseVersionControlRequirementSerializer,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginContributorSerializer',
    'PluginCreateReleaseSerializer',
    'PluginCreateSerializer',
    'PluginGameSerializer',
    'PluginImageSerializer',
    'PluginReleaseDownloadRequirementSerializer',
    'PluginReleasePackageRequirementSerializer',
    'PluginReleasePyPiRequirementSerializer',
    'PluginReleaseSerializer',
    'PluginReleaseVersionControlRequirementSerializer',
    'PluginSerializer',
    'PluginTagSerializer',
    'SubPluginPathSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class PluginImageSerializer(ProjectImageSerializer):
    """Serializer for adding, removing, and listing Plugin images."""

    class Meta(ProjectImageSerializer.Meta):
        """Define metaclass attributes."""

        model = PluginImage


class PluginReleasePackageRequirementSerializer(
    ReleasePackageRequirementSerializer
):
    """Serializer for Plugin Release Package requirements."""

    class Meta(ReleasePackageRequirementSerializer.Meta):
        """Define metaclass attributes."""

        model = PluginReleasePackageRequirement


class PluginReleaseDownloadRequirementSerializer(
    ReleaseDownloadRequirementSerializer
):
    """Serializer for Plugin Release Download requirements."""

    class Meta(ReleaseDownloadRequirementSerializer.Meta):
        """Define metaclass attributes."""

        model = PluginReleaseDownloadRequirement


class PluginReleasePyPiRequirementSerializer(ReleasePyPiRequirementSerializer):
    """Serializer for Plugin Release PyPi requirements."""

    class Meta(ReleasePyPiRequirementSerializer.Meta):
        """Define metaclass attributes."""

        model = PluginReleasePyPiRequirement


class PluginReleaseVersionControlRequirementSerializer(
    ReleaseVersionControlRequirementSerializer
):
    """Serializer for Plugin Release VCS requirements."""

    class Meta(ReleaseVersionControlRequirementSerializer.Meta):
        """Define metaclass attributes."""

        model = PluginReleaseVersionControlRequirement


class PluginReleaseSerializer(PluginReleaseBase, ProjectReleaseSerializer):
    """Serializer for listing Plugin releases."""

    download_requirements = PluginReleaseDownloadRequirementSerializer(
        source='pluginreleasedownloadrequirement_set',
        read_only=True,
        many=True,
    )
    package_requirements = PluginReleasePackageRequirementSerializer(
        source='pluginreleasepackagerequirement_set',
        read_only=True,
        many=True,
    )
    pypi_requirements = PluginReleasePyPiRequirementSerializer(
        source='pluginreleasepypirequirement_set',
        read_only=True,
        many=True,
    )
    vcs_requirements = PluginReleaseVersionControlRequirementSerializer(
        source='pluginreleaseversioncontrolrequirement_set',
        read_only=True,
        many=True,
    )

    class Meta(ProjectReleaseSerializer.Meta):
        """Define metaclass attributes."""

        model = PluginRelease


class PluginCreateReleaseSerializer(
    PluginReleaseBase, ProjectCreateReleaseSerializer
):
    """Serializer for creating and retrieving Plugin releases."""

    class Meta(ProjectCreateReleaseSerializer.Meta):
        """Define metaclass attributes."""

        model = PluginRelease


class PluginSerializer(ProjectSerializer):
    """Serializer for updating and listing Plugins."""

    project_type = 'plugin'
    release_model = PluginRelease

    class Meta(ProjectSerializer.Meta):
        """Define metaclass attributes."""

        model = Plugin


class PluginCreateSerializer(PluginSerializer):
    """Serializer for creating Plugins."""

    releases = PluginCreateReleaseSerializer(
        write_only=True,
    )

    class Meta(PluginSerializer.Meta):
        """Define metaclass attributes."""

        fields = PluginSerializer.Meta.fields + (
            'releases',
        )


class PluginGameSerializer(ProjectGameSerializer):
    """Supported Games Serializer for Plugins."""

    class Meta(ProjectGameSerializer.Meta):
        """Define metaclass attributes."""

        model = PluginGame


class PluginTagSerializer(ProjectTagSerializer):
    """Tags Serializer for Plugins."""

    class Meta(ProjectTagSerializer.Meta):
        """Define metaclass attributes."""

        model = PluginTag


class PluginContributorSerializer(ProjectContributorSerializer):
    """Contributors Serializer for Plugins."""

    class Meta(ProjectContributorSerializer.Meta):
        """Define metaclass attributes."""

        model = PluginContributor


class SubPluginPathSerializer(ProjectThroughMixin):
    """Sub-Plugin Paths Serializer."""

    class Meta:
        """Define metaclass attributes."""

        model = SubPluginPath
        fields = (
            'allow_module',
            'allow_package_using_basename',
            'allow_package_using_init',
            'path',
        )

    def get_field_names(self, declared_fields, info):
        """Remove 'path' from the PATCH field names."""
        field_names = super().get_field_names(
            declared_fields=declared_fields,
            info=info,
        )
        if self.context['request'].method == 'PATCH':
            field_names = list(field_names)
            field_names.remove('path')
            field_names = tuple(field_names)
        return field_names

    def validate(self, attrs):
        """Validate that at least one of the 'Allow' fields is True."""
        if not any([
            attrs['allow_module'],
            attrs['allow_package_using_basename'],
            attrs['allow_package_using_init'],
        ]):
            message = "At least one of the 'Allow' fields must be True."
            raise ValidationError({
                'allow_module': message,
                'allow_package_using_basename': message,
                'allow_package_using_init': message,
            })
        return super().validate(attrs=attrs)
