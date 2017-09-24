"""Plugin serializers for APIs."""

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
from project_manager.plugins.helpers import get_plugin_basename
from project_manager.plugins.models import Plugin, PluginImage, PluginRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
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


class PluginReleaseListSerializer(ProjectReleaseListSerializer):
    """Serializer for listing Plugin releases."""

    class Meta(ProjectReleaseListSerializer.Meta):
        model = PluginRelease


class PluginReleaseSerializer(ProjectReleaseSerializer):
    """Serializer for creating and retrieving Plugin releases."""

    project_class = Plugin
    project_type = 'plugin'

    class Meta(ProjectReleaseSerializer.Meta):
        model = PluginRelease

    @property
    def zip_parser(self):
        return get_plugin_basename


class PluginSerializer(ProjectSerializer):
    """Serializer for updating and listing Plugins."""

    project_type = 'plugin'
    release_model = PluginRelease

    class Meta(ProjectSerializer.Meta):
        model = Plugin


class PluginCreateSerializer(PluginSerializer):
    """Serializer for creating Plugins."""

    releases = PluginReleaseSerializer(
        write_only=True,
    )

    class Meta(PluginSerializer.Meta):
        fields = PluginSerializer.Meta.fields + (
            'releases',
        )
