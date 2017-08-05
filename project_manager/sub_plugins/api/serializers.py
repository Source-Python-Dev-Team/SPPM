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
# TODO:     paths
# TODO:     supported_games
# TODO:     tags
class SubPluginImageSerializer(ModelSerializer):
    class Meta:
        model = SubPluginImage
        fields = (
            'image',
        )


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

        if zip_file is None:
            return attrs

        kwargs = self.context['view'].kwargs
        plugin_slug = kwargs.get('plugin_slug', None)
        # TODO: figure out if this try/except is necessary
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
        except Plugin.DoesNotExist:
            raise ValidationError(f'Plugin "{plugin_slug}" not found.')

        # Validate the version is new for the sub_plugin
        try:
            sub_plugin = SubPlugin.objects.get(
                slug=kwargs['slug'],
            )
            sub_plugin_basename = sub_plugin.basename
        except (SubPlugin.DoesNotExist, KeyError):
            sub_plugin_basename = None
        else:
            if SubPluginRelease.objects.filter(
                sub_plugin=sub_plugin,
                version=version,
            ).exists():
                raise ValidationError({
                    'version': 'Given version matches existing version.',
                })

        if zip_file is not None:
            basename = get_sub_plugin_basename(zip_file, plugin)
            if basename != sub_plugin_basename:
                raise ValidationError({
                    'zip_file': (
                        f"Basename in zip '{basename}' does not match "
                        f"basename for sub_plugin '{sub_plugin_basename}'"
                    )
                })
        return attrs


class SubPluginSerializer(ProjectSerializer):
    images = SubPluginImageSerializer(
        many=True,
        read_only=True,
    )
    releases = SubPluginReleaseSerializer(write_only=True)
    reverse_path = 'sub-plugin'

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

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        action = self.context['view'].action
        if action == 'update':
            name_kwargs = extra_kwargs.get('name', {})
            name_kwargs['read_only'] = True
            extra_kwargs['name'] = name_kwargs
        return extra_kwargs

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
