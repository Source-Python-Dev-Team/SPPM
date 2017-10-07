"""SubPlugin serializers for APIs."""

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
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginContributor,
    SubPluginGame,
    SubPluginImage,
    SubPluginRelease,
    SubPluginTag,
)
from .mixins import SubPluginReleaseBase


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginContributorSerializer',
    'SubPluginCreateReleaseSerializer',
    'SubPluginCreateSerializer',
    'SubPluginGameSerializer',
    'SubPluginImageSerializer',
    'SubPluginReleaseSerializer',
    'SubPluginSerializer',
    'SubPluginTagSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class SubPluginImageSerializer(ProjectImageSerializer):
    """Serializer for adding, removing, and listing SubPlugin images."""

    class Meta(ProjectImageSerializer.Meta):
        model = SubPluginImage


class SubPluginReleaseSerializer(
    SubPluginReleaseBase, ProjectReleaseSerializer
):
    """Serializer for listing Plugin releases."""

    class Meta(ProjectReleaseSerializer.Meta):
        model = SubPluginRelease


class SubPluginCreateReleaseSerializer(
    SubPluginReleaseBase, ProjectCreateReleaseSerializer
):
    """Serializer for creating and listing SubPlugin releases."""

    class Meta(ProjectCreateReleaseSerializer.Meta):
        model = SubPluginRelease


class SubPluginSerializer(ProjectSerializer):
    """Serializer for updating and listing SubPlugins."""

    project_type = 'sub-plugin'
    release_model = SubPluginRelease

    class Meta(ProjectSerializer.Meta):
        model = SubPlugin

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

    @staticmethod
    def get_download_kwargs(obj, release):
        """Return the release's reverse kwargs."""
        return {
            'slug': obj.plugin.slug,
            'sub_plugin_slug': obj.slug,
            'zip_file': release.file_name,
        }

    def get_extra_validated_data(self, validated_data):
        """Add any extra data to be used on create."""
        validated_data = super().get_extra_validated_data(validated_data)
        validated_data['plugin'] = self.parent_project
        return validated_data


class SubPluginCreateSerializer(SubPluginSerializer):
    """Serializer for creating SubPlugins."""

    releases = SubPluginCreateReleaseSerializer(
        write_only=True,
    )

    class Meta(SubPluginSerializer.Meta):
        fields = SubPluginSerializer.Meta.fields + (
            'releases',
        )


class SubPluginGameSerializer(ProjectGameSerializer):
    """Supported Games Serializer for SubPlugins."""

    class Meta(ProjectGameSerializer.Meta):
        model = SubPluginGame


class SubPluginTagSerializer(ProjectTagSerializer):
    """Tags Serializer for SubPlugins."""

    class Meta(ProjectTagSerializer.Meta):
        model = SubPluginTag


class SubPluginContributorSerializer(ProjectContributorSerializer):
    """Contributors Serializer for SubPlugins."""

    class Meta(ProjectContributorSerializer.Meta):
        model = SubPluginContributor