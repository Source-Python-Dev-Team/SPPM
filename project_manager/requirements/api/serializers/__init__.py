"""Requirement serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from project_manager.users.api.serializers import (
    PackageContributionSerializer,
    PluginContributionSerializer,
    SubPluginContributionSerializer,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'DownloadRequirementSerializer',
    'PyPiRequirementSerializer',
    'RequirementSerializer',
    'VersionControlRequirementSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class RequirementSerializer(ModelSerializer):
    """Base serializer for listing requirements."""

    required_in_package_releases = PackageContributionSerializer(
        many=True,
        read_only=True,
    )
    required_in_plugin_releases = PluginContributionSerializer(
        many=True,
        read_only=True,
    )
    required_in_sub_plugin_releases = SubPluginContributionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        fields = (
            'required_in_package_releases',
            'required_in_plugin_releases',
            'required_in_sub_plugin_releases',
        )


class DownloadRequirementSerializer(RequirementSerializer):
    """Serializer for listing Download requirements."""

    class Meta(RequirementSerializer):
        model = DownloadRequirement
        fields = (
            'name',
            'description',
            'url',
        ) + RequirementSerializer.Meta.fields


class PyPiRequirementSerializer(RequirementSerializer):
    """Serializer for listing PyPi requirements."""

    class Meta(RequirementSerializer):
        model = PyPiRequirement
        fields = (
            'name',
        ) + RequirementSerializer.Meta.fields


class VersionControlRequirementSerializer(RequirementSerializer):
    """Serializer for listing Version Control requirements."""

    class Meta(RequirementSerializer):
        model = VersionControlRequirement
        fields = (
            'url',
        ) + RequirementSerializer.Meta.fields
