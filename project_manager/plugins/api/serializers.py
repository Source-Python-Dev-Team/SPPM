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
from project_manager.plugins.models import (
    Plugin,
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginRelease,
    PluginTag,
    SubPluginPath,
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
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
# TODO: APIs for adding/removing paths
class PluginImageSerializer(ProjectImageSerializer):
    """Serializer for adding, removing, and listing Plugin images."""

    class Meta(ProjectImageSerializer.Meta):
        model = PluginImage


class PluginReleaseSerializer(PluginReleaseBase, ProjectReleaseSerializer):
    """Serializer for listing Plugin releases."""

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
    """"""

    class Meta:
        model = SubPluginPath
        fields = (
            'allow_module',
            'allow_package_using_basename',
            'allow_package_using_init',
            'path',
        )

    def validate(self, attrs):
        """"""
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
