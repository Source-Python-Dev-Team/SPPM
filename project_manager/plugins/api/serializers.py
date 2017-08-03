# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# 3rd-Party Django
from rest_framework.fields import (
    CharField,
    FileField,
    SerializerMethodField,
)
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

# App
from ..helpers import get_plugin_basename
from ..models import Plugin, PluginImage, PluginRelease
from project_manager.common.helpers import get_date_display
from project_manager.games.api.serializers import GameSerializer
from project_manager.packages.api.serializers import (
    PackageRequirementSerializer,
)
from project_manager.requirements.api.serializers import (
    DownloadRequirementSerializer,
    PyPiRequirementSerializer,
    VersionControlRequirementSerializer,
)
from project_manager.tags.api.serializers import TagSerializer
from project_manager.users.api.serializers import ForumUserSerializer


# =============================================================================
# >> SERIALIZERS
# =============================================================================
# TODO: APIs
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


class PluginSerializer(ModelSerializer):
    current_release = SerializerMethodField()
    owner = ForumUserSerializer(
        read_only=True,
    )
    contributors = ForumUserSerializer(
        many=True,
        read_only=True,
    )
    created = SerializerMethodField()
    updated = SerializerMethodField()
    package_requirements = PackageRequirementSerializer(
        many=True,
        read_only=True,
    )
    download_requirements = DownloadRequirementSerializer(
        many=True,
        read_only=True,
    )
    pypi_requirements = PyPiRequirementSerializer(
        many=True,
        read_only=True,
    )
    vcs_requirements = VersionControlRequirementSerializer(
        many=True,
        read_only=True,
    )
    supported_games = GameSerializer(
        many=True,
        read_only=True,
    )
    images = PluginImageSerializer(
        many=True,
        read_only=True,
    )
    tags = TagSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Plugin
        """
            TODO: add the following:

                tags
        """
        fields = (
            'name',
            'slug',
            'total_downloads',
            'current_release',
            'created',
            'updated',
            'synopsis',
            'description',
            'configuration',
            'logo',
            'owner',
            'contributors',
            'package_requirements',
            'download_requirements',
            'pypi_requirements',
            'vcs_requirements',
            'supported_games',
            'images',
            'tags',
        )
        read_only_fields = (
            'slug',
        )

    def get_current_release(self, obj):
        try:
            release = obj.releases.all()[0]
        except IndexError:
            return {}
        zip_url = reverse(
            viewname='plugin-download',
            kwargs={
                'slug': obj.slug,
                'zip_file': release.file_name,
            },
            request=self.context['request']
        )
        return {
            'version': release.version,
            'notes': str(release.notes) if release.notes else release.notes,
            'zip_file': zip_url,
        }

    def get_created(self, obj):
        return self.get_date_time_dict(timestamp=obj.created)

    def get_updated(self, obj):
        try:
            release = obj.releases.all()[0]
        except IndexError:
            return self.get_date_time_dict(timestamp=obj.created)
        return self.get_date_time_dict(timestamp=release.modified)

    @staticmethod
    def get_date_time_dict(timestamp):
        return {
            'actual': timestamp,
            'locale': get_date_display(
                date=timestamp,
                date_format='DATE_FORMAT',
            ),
            'locale_short': get_date_display(
                date=timestamp,
                date_format='SHORT_DATE_FORMAT',
            )
        }


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
