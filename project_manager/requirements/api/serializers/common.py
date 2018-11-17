"""Requirement serializers for APIs in other apps."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ReleaseDownloadRequirementSerializer',
    'ReleasePyPiRequirementSerializer',
    'ReleaseVersionControlRequirementSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class ReleaseDownloadRequirementSerializer(ModelSerializer):
    """Serializer for listing required downloads for projects."""

    url = ReadOnlyField(source='download_requirement.url')

    class Meta:
        fields = (
            'url',
            'optional',
        )


class ReleasePyPiRequirementSerializer(ModelSerializer):
    """Serializer for listing required PyPis for projects."""

    name = ReadOnlyField(source='pypi_requirement.name')
    slug = ReadOnlyField(source='pypi_requirement.slug')
    version = ReadOnlyField()

    class Meta:
        fields = (
            'name',
            'slug',
            'version',
            'optional',
        )


class ReleaseVersionControlRequirementSerializer(ModelSerializer):
    """Serializer for listing required VCS for projects."""

    url = ReadOnlyField(source='vcs_requirement.url')
    version = ReadOnlyField()

    class Meta:
        fields = (
            'name',
            'type',
            'url',
            'version',
            'optional',
        )
