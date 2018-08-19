"""Plugin serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
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
from project_manager.requirements.api.serializers.common import (
    ReleaseDownloadRequirementSerializer,
    ReleasePyPiRequirementSerializer,
    ReleaseVersionControlRequirementSerializer,
)
from .mixins import PluginReleaseBase


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginContributorSerializer',
    'PluginCreateReleaseSerializer',
    'PluginCreateSerializer',
    'PluginGameSerializer',
    'PluginImageSerializer',
    'PluginReleaseSerializer',
    'PluginSerializer',
    'PluginTagSerializer',
    'SubPluginPathSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
# TODO: APIs for adding/removing paths
class PluginImageSerializer(ProjectImageSerializer):
    """Serializer for adding, removing, and listing Plugin images."""

    class Meta(ProjectImageSerializer.Meta):
        model = PluginImage


class PluginReleasePackageRequirementSerializer(
    ReleasePackageRequirementSerializer
):
    """"""

    class Meta(ReleasePackageRequirementSerializer.Meta):
        model = PluginReleasePackageRequirement


class PluginReleaseDownloadRequirementSerializer(
    ReleaseDownloadRequirementSerializer
):
    """"""

    class Meta(ReleaseDownloadRequirementSerializer.Meta):
        model = PluginReleaseDownloadRequirement


class PluginReleasePyPiRequirementSerializer(ReleasePyPiRequirementSerializer):
    """"""

    class Meta(ReleasePyPiRequirementSerializer.Meta):
        model = PluginReleasePyPiRequirement


class PluginReleaseVersionControlRequirementSerializer(
    ReleaseVersionControlRequirementSerializer
):
    """"""

    class Meta(ReleaseVersionControlRequirementSerializer.Meta):
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
        model = PluginRelease


class PluginCreateReleaseSerializer(
    PluginReleaseBase, ProjectCreateReleaseSerializer
):
    """Serializer for creating and retrieving Plugin releases."""

    class Meta(ProjectCreateReleaseSerializer.Meta):
        model = PluginRelease


class PluginSerializer(ProjectSerializer):
    """Serializer for updating and listing Plugins."""

    project_type = 'plugin'
    release_model = PluginRelease

    class Meta(ProjectSerializer.Meta):
        model = Plugin


class PluginCreateSerializer(PluginSerializer):
    """Serializer for creating Plugins."""

    releases = PluginCreateReleaseSerializer(
        write_only=True,
    )

    class Meta(PluginSerializer.Meta):
        fields = PluginSerializer.Meta.fields + (
            'releases',
        )


class PluginGameSerializer(ProjectGameSerializer):
    """Supported Games Serializer for Plugins."""

    class Meta(ProjectGameSerializer.Meta):
        model = PluginGame


class PluginTagSerializer(ProjectTagSerializer):
    """Tags Serializer for Plugins."""

    class Meta(ProjectTagSerializer.Meta):
        model = PluginTag


class PluginContributorSerializer(ProjectContributorSerializer):
    """Contributors Serializer for Plugins."""

    class Meta(ProjectContributorSerializer.Meta):
        model = PluginContributor


class SubPluginPathSerializer(ProjectThroughMixin):
    """Sub-Plugin Paths Serializer."""

    class Meta:
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
