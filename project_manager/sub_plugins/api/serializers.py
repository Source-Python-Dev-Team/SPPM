# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# 3rd-Party Django
from rest_framework.fields import CharField, FileField
from rest_framework.serializers import ModelSerializer

# App
from project_manager.common.api.serializers import ProjectSerializer
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
# TODO:     paths
# TODO:     supported_games
# TODO:     tags
class SubPluginImageSerializer(ModelSerializer):
    class Meta:
        model = SubPluginImage
        fields = (
            'image',
        )


class SubPluginSerializer(ProjectSerializer):
    reverse_path = 'sub-plugin'

    images = SubPluginImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta(ProjectSerializer.Meta):
        model = SubPlugin
        fields = ProjectSerializer.Meta.fields + (
            'images',
        )

    @staticmethod
    def get_download_kwargs(obj, release):
        return {
            'slug': obj.plugin.slug,
            'sub_plugin_slug': obj.slug,
            'zip_file': release.file_name,
        }


class SubPluginReleaseSerializer(ModelSerializer):
    notes = CharField(max_length=512, allow_blank=True)
    version = CharField(max_length=8, allow_blank=True)
    zip_file = FileField(allow_null=True)

    class Meta:
        model = SubPluginRelease
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

        # Validate the version is new for the sub_plugin
        try:
            sub_plugin = SubPlugin.objects.get(pk=self.context['view'].kwargs['pk'])
            sub_plugin_basename = sub_plugin.basename
        except SubPlugin.DoesNotExist:
            sub_plugin_basename = None
        else:
            if SubPluginRelease.objects.filter(
                sub_plugin=sub_plugin,
                version=version,
            ).exists():
                raise ValidationError({
                    'version': 'Given version matches existing version.',
                })

        basename = get_sub_plugin_basename(zip_file)
        if basename != sub_plugin_basename:
            raise ValidationError({
                'zip_file': (
                    f"Basename in zip '{basename}' does not match basename "
                    f"for sub_plugin '{sub_plugin_basename}'"
                )
            })
        return attrs


class SubPluginCreateSerializer(SubPluginSerializer):
    releases = SubPluginReleaseSerializer(write_only=True)

    class Meta(SubPluginSerializer.Meta):
        fields = SubPluginSerializer.Meta.fields + ('releases',)
        read_only_fields = SubPluginSerializer.Meta.read_only_fields

    def validate(self, attrs):
        release_dict = attrs.get('releases', {})
        version = release_dict.get('version', '')
        zip_file = release_dict.get('zip_file')
        if not all([version, zip_file]):
            raise ValidationError({
                'releases': (
                    'Version and Zip File are required when creating '
                    'a sub_plugin.'
                )
            })

    def create(self, validated_data):
        release_dict = validated_data.pop('releases', {})
        version = release_dict['version']
        zip_file = release_dict['zip_file']
        notes = release_dict['notes']
        instance = super().create(validated_data)
        SubPluginRelease.objects.create(
            sub_plugin=instance,
            notes=notes,
            version=version,
            zip_file=zip_file,
        )
        return instance


class SubPluginUpdateSerializer(SubPluginCreateSerializer):

    class Meta(SubPluginCreateSerializer.Meta):
        read_only_fields = SubPluginCreateSerializer.Meta.read_only_fields + (
            'name',
        )

    def update(self, instance, validated_data):
        release_dict = validated_data.pop('releases', {})
        version = release_dict.get('version', '')
        zip_file = release_dict.get('zip_file')
        if all([version, zip_file]):
            notes = release_dict.get('notes', '')
            SubPluginRelease.objects.create(
                sub_plugin=instance,
                notes=notes,
                version=version,
                zip_file=zip_file,
            )

        super().update(
            instance=instance,
            validated_data=validated_data,
        )

        return instance
