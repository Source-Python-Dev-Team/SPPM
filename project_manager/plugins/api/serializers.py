# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# 3rd-Party Django
from rest_framework.fields import CharField, FileField
from rest_framework.serializers import ModelSerializer

# App
from ..helpers import get_plugin_basename
from ..models import Plugin, PluginImage, PluginRelease
from project_manager.common.api.mixins import ProjectSerializer


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


class PluginSerializer(ProjectSerializer):
    reverse_path = 'plugin'

    images = PluginImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta(ProjectSerializer.Meta):
        model = Plugin
        fields = ProjectSerializer.Meta.fields + (
            'images',
        )


class PluginReleaseSerializer(ModelSerializer):
    notes = CharField(max_length=512, allow_blank=True)
    version = CharField(max_length=8, allow_blank=True)
    zip_file = FileField(allow_null=True)

    class Meta:
        model = PluginRelease
        fields = (
            'notes',
            'zip_file',
            'version',
        )

    def validate(self, attrs):
        version = attrs.get('version', '')
        zip_file = attrs.get('zip_file')
        if any([version, zip_file]) and not all([version, zip_file]):
            raise ValidationError({
                '__all__': (
                    "If either 'version' or 'zip_file' are provided, "
                    "must be provided."
                )
            })

        # Validate the version is new for the plugin
        try:
            plugin = Plugin.objects.get(pk=self.context['view'].kwargs['pk'])
            plugin_basename = plugin.basename
        except Plugin.DoesNotExist:
            plugin_basename = None
        else:
            if PluginRelease.objects.filter(
                plugin=plugin,
                version=version,
            ).exists():
                raise ValidationError({
                    'version': 'Given version matches existing version.',
                })

        basename = get_plugin_basename(zip_file)
        if basename != plugin_basename:
            raise ValidationError({
                'zip_file': (
                    f"Basename in zip '{basename}' does not match basename "
                    f"for plugin '{plugin_basename}'"
                )
            })
        return attrs


class PluginCreateSerializer(PluginSerializer):
    releases = PluginReleaseSerializer(write_only=True)

    class Meta(PluginSerializer.Meta):
        fields = PluginSerializer.Meta.fields + ('releases', )
        read_only_fields = PluginSerializer.Meta.read_only_fields

    def validate(self, attrs):
        release_dict = attrs.get('releases', {})
        version = release_dict.get('version', '')
        zip_file = release_dict.get('zip_file')
        if not all([version, zip_file]):
            raise ValidationError({
                'releases': (
                    'Version and Zip File are required when creating a plugin.'
                )
            })

    def create(self, validated_data):
        release_dict = validated_data.pop('releases', {})
        version = release_dict['version']
        zip_file = release_dict['zip_file']
        notes = release_dict['notes']
        instance = super().create(validated_data)
        PluginRelease.objects.create(
            plugin=instance,
            notes=notes,
            version=version,
            zip_file=zip_file,
        )
        return instance


class PluginUpdateSerializer(PluginCreateSerializer):

    class Meta(PluginCreateSerializer.Meta):
        read_only_fields = PluginCreateSerializer.Meta.read_only_fields + (
            'name',
        )

    def update(self, instance, validated_data):
        release_dict = validated_data.pop('releases', {})
        version = release_dict.get('version', '')
        zip_file = release_dict.get('zip_file')
        if all([version, zip_file]):
            notes = release_dict.get('notes', '')
            PluginRelease.objects.create(
                plugin=instance,
                notes=notes,
                version=version,
                zip_file=zip_file,
            )

        super().update(
            instance=instance,
            validated_data=validated_data,
        )

        return instance
