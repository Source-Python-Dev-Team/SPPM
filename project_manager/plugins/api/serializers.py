"""Plugin serializers for APIs."""

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
from project_manager.plugins.models import Plugin, PluginImage, PluginRelease
from .mixins import PluginReleaseBase


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginCreateSerializer',
    'PluginCreateReleaseSerializer',
    'PluginImageSerializer',
    'PluginReleaseSerializer',
    'PluginSerializer',
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
