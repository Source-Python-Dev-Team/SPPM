# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.common.api.serializers import (
    ProjectReleaseSerializer,
    ProjectSerializer,
)
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.helpers import get_sub_plugin_basename
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginImage,
    SubPluginRelease,
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
# TODO: APIs
# TODO:     contributors
# TODO:     images
# TODO:     supported_games
# TODO:     tags
class SubPluginImageSerializer(ModelSerializer):
    class Meta:
        model = SubPluginImage
        fields = (
            'image',
        )


class SubPluginReleaseSerializer(ProjectReleaseSerializer):
    project_class = SubPlugin
    project_type = 'sub-plugin'
    slug_kwarg = 'slug'
    zip_parser = get_sub_plugin_basename

    class Meta(ProjectReleaseSerializer.Meta):
        model = SubPluginRelease

    @property
    def parent_project(self):
        kwargs = self.context['view'].kwargs
        plugin_slug = kwargs.get('plugin_slug')
        # TODO: figure out if this try/except is necessary
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
        except Plugin.DoesNotExist:
            raise ValidationError(f'Plugin "{plugin_slug}" not found.')
        return plugin

    def get_project_kwargs(self, parent_project=None):
        kwargs = self.context['view'].kwargs
        return {
            'slug': kwargs.get('slug'),
            'plugin': parent_project,
        }


class SubPluginSerializer(ProjectSerializer):
    images = SubPluginImageSerializer(
        many=True,
        read_only=True,
    )
    releases = SubPluginReleaseSerializer(
        write_only=True,
    )

    project_type = 'sub-plugin'
    release_model = SubPluginRelease

    class Meta(ProjectSerializer.Meta):
        model = SubPlugin
        fields = ProjectSerializer.Meta.fields + (
            'images',
            'releases',
        )

    @staticmethod
    def get_download_kwargs(obj, release):
        return {
            'slug': obj.plugin.slug,
            'sub_plugin_slug': obj.slug,
            'zip_file': release.file_name,
        }
