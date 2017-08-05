# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.common.api.serializers import (
    ProjectReleaseSerializer,
    ProjectSerializer,
)
from project_manager.plugins.helpers import get_plugin_basename
from project_manager.plugins.models import Plugin, PluginImage, PluginRelease


# =============================================================================
# >> SERIALIZERS
# =============================================================================
# TODO: APIs for adding/removing
# TODO:     contributors
# TODO:     images
# TODO:     paths
# TODO:     supported_games
# TODO:     tags
class PluginImageSerializer(ModelSerializer):
    class Meta:
        model = PluginImage
        fields = (
            'image',
        )


class PluginReleaseSerializer(ProjectReleaseSerializer):
    project_class = Plugin
    project_type = 'plugin'
    zip_parser = get_plugin_basename

    class Meta(ProjectReleaseSerializer.Meta):
        model = PluginRelease


class PluginSerializer(ProjectSerializer):
    images = PluginImageSerializer(
        many=True,
        read_only=True,
    )
    releases = PluginReleaseSerializer(
        write_only=True,
    )

    project_type = 'plugin'
    release_model = PluginRelease

    class Meta(ProjectSerializer.Meta):
        model = Plugin
        fields = ProjectSerializer.Meta.fields + (
            'images',
            'releases',
        )
