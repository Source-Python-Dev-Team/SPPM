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
from project_manager.packages.api.serializers.common import (
    ReleasePackageRequirementSerializer,
)
from project_manager.plugins.models import Plugin
from project_manager.requirements.api.serializers.common import (
    ReleaseDownloadRequirementSerializer,
    ReleasePyPiRequirementSerializer,
    ReleaseVersionControlRequirementSerializer,
)
from project_manager.sub_plugins.api.serializers.mixins import (
    SubPluginReleaseBase,
)
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginContributor,
    SubPluginGame,
    SubPluginImage,
    SubPluginRelease,
    SubPluginReleaseDownloadRequirement,
    SubPluginReleasePackageRequirement,
    SubPluginReleasePyPiRequirement,
    SubPluginReleaseVersionControlRequirement,
    SubPluginTag,
)


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
    'SubPluginReleaseDownloadRequirementSerializer',
    'SubPluginReleasePackageRequirementSerializer',
    'SubPluginReleasePyPiRequirementSerializer',
    'SubPluginSerializer',
    'SubPluginReleaseVersionControlRequirementSerializer',
    'SubPluginTagSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class SubPluginImageSerializer(ProjectImageSerializer):
    """Serializer for adding, removing, and listing SubPlugin images."""

    class Meta(ProjectImageSerializer.Meta):
        """Define metaclass attributes."""

        model = SubPluginImage


class SubPluginReleasePackageRequirementSerializer(
    ReleasePackageRequirementSerializer
):
    """Serializer for SubPlugin Release Package requirements."""

    class Meta(ReleasePackageRequirementSerializer.Meta):
        """Define metaclass attributes."""

        model = SubPluginReleasePackageRequirement


class SubPluginReleaseDownloadRequirementSerializer(
    ReleaseDownloadRequirementSerializer
):
    """Serializer for SubPlugin Release Download requirements."""

    class Meta(ReleaseDownloadRequirementSerializer.Meta):
        """Define metaclass attributes."""

        model = SubPluginReleaseDownloadRequirement


class SubPluginReleasePyPiRequirementSerializer(
    ReleasePyPiRequirementSerializer
):
    """Serializer for SubPlugin Release PyPi requirements."""

    class Meta(ReleasePyPiRequirementSerializer.Meta):
        """Define metaclass attributes."""

        model = SubPluginReleasePyPiRequirement


class SubPluginReleaseVersionControlRequirementSerializer(
    ReleaseVersionControlRequirementSerializer
):
    """Serializer for SubPlugin Release VCS requirements."""

    class Meta(ReleaseVersionControlRequirementSerializer.Meta):
        """Define metaclass attributes."""

        model = SubPluginReleaseVersionControlRequirement


class SubPluginReleaseSerializer(
    SubPluginReleaseBase, ProjectReleaseSerializer
):
    """Serializer for listing Plugin releases."""

    download_requirements = SubPluginReleaseDownloadRequirementSerializer(
        source='subpluginreleasedownloadrequirement_set',
        read_only=True,
        many=True,
    )
    package_requirements = SubPluginReleasePackageRequirementSerializer(
        source='subpluginreleasepackagerequirement_set',
        read_only=True,
        many=True,
    )
    pypi_requirements = SubPluginReleasePyPiRequirementSerializer(
        source='subpluginreleasepypirequirement_set',
        read_only=True,
        many=True,
    )
    vcs_requirements = SubPluginReleaseVersionControlRequirementSerializer(
        source='subpluginreleaseversioncontrolrequirement_set',
        read_only=True,
        many=True,
    )

    class Meta(ProjectReleaseSerializer.Meta):
        """Define metaclass attributes."""

        model = SubPluginRelease


class SubPluginCreateReleaseSerializer(
    SubPluginReleaseBase, ProjectCreateReleaseSerializer
):
    """Serializer for creating and listing SubPlugin releases."""

    class Meta(ProjectCreateReleaseSerializer.Meta):
        """Define metaclass attributes."""

        model = SubPluginRelease


class SubPluginSerializer(ProjectSerializer):
    """Serializer for updating and listing SubPlugins."""

    project_type = 'sub-plugin'
    release_model = SubPluginRelease

    class Meta(ProjectSerializer.Meta):
        """Define metaclass attributes."""

        model = SubPlugin

    @property
    def parent_project(self):
        """Return the parent plugin."""
        kwargs = self.context['view'].kwargs
        plugin_slug = kwargs.get('plugin_slug')
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
        except Plugin.DoesNotExist:
            raise ValidationError(
                f"Plugin '{plugin_slug}' not found."
            ) from Plugin.DoesNotExist
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
        """Define metaclass attributes."""

        fields = SubPluginSerializer.Meta.fields + (
            'releases',
        )


class SubPluginGameSerializer(ProjectGameSerializer):
    """Supported Games Serializer for SubPlugins."""

    class Meta(ProjectGameSerializer.Meta):
        """Define metaclass attributes."""

        model = SubPluginGame


class SubPluginTagSerializer(ProjectTagSerializer):
    """Tags Serializer for SubPlugins."""

    class Meta(ProjectTagSerializer.Meta):
        """Define metaclass attributes."""

        model = SubPluginTag


class SubPluginContributorSerializer(ProjectContributorSerializer):
    """Contributors Serializer for SubPlugins."""

    class Meta(ProjectContributorSerializer.Meta):
        """Define metaclass attributes."""

        model = SubPluginContributor
