# =============================================================================
# >> IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.plugins.models import Plugin, PluginRelease


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class ReleaseSerializer(ModelSerializer):

    class Meta:
        model = PluginRelease
        fields = (
            'version', 'notes', 'zip_file', 'created', 'modified',
        )


class PluginListSerializer(ModelSerializer):
    releases = ReleaseSerializer(many=True)

    class Meta:
        model = Plugin
        fields = (
            'name', 'slug', 'logo', 'synopsis', 'releases',
        )
        read_only_fields = ('slug', )


class PluginSerializer(PluginListSerializer):
    class Meta(PluginListSerializer.Meta):
        fields = PluginListSerializer.Meta.fields + (
            'description',
        )
