"""SubPlugin serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# App
from project_manager.common.api.serializers import (
    ProjectImageSerializer,
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
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginImageSerializer',
    'SubPluginReleaseSerializer',
    'SubPluginSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class SubPluginImageSerializer(ProjectImageSerializer):
    """Serializer for adding, removing, and listing SubPlugin images."""

    class Meta(ProjectImageSerializer.Meta):
        model = SubPluginImage


class SubPluginReleaseSerializer(ProjectReleaseSerializer):
    """Serializer for creating and listing SubPlugin releases."""

    project_class = SubPlugin
    project_type = 'sub-plugin'
    slug_kwarg = 'slug'
    zip_parser = get_sub_plugin_basename

    class Meta(ProjectReleaseSerializer.Meta):
        model = SubPluginRelease

    @property
    def parent_project(self):
        """Return the parent plugin."""
        kwargs = self.context['view'].kwargs
        plugin_slug = kwargs.get('plugin_slug')
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
        except Plugin.DoesNotExist:
            raise ValidationError(f"Plugin '{plugin_slug}' not found.")
        return plugin

    def get_project_kwargs(self, parent_project=None):
        """Return kwargs for the project."""
        kwargs = self.context['view'].kwargs
        return {
            'slug': kwargs.get('slug'),
            'plugin': parent_project,
        }


class SubPluginSerializer(ProjectSerializer):
    """Serializer for creating, updating, and listing SubPlugins."""

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
        """Return the release's reverse kwargs."""
        return {
            'slug': obj.plugin.slug,
            'sub_plugin_slug': obj.slug,
            'zip_file': release.file_name,
        }
