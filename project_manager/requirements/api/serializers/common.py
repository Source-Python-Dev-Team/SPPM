"""Requirement serializers for APIs in other apps."""

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


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'RequiredDownloadSerializer',
    'RequiredPyPiSerializer',
    'RequiredVersionControlSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class RequiredDownloadSerializer(ModelSerializer):
    """Serializer for listing required Downloads for projects."""

    class Meta:
        model = DownloadRequirement
        fields = (
            'name',
            'description',
            'url',
        )


class RequiredPyPiSerializer(ModelSerializer):
    """Serializer for listing required PyPis for projects."""

    class Meta:
        model = PyPiRequirement
        fields = (
            'name',
        )


class RequiredVersionControlSerializer(ModelSerializer):
    """Serializer for listing required VCS for projects."""

    class Meta:
        model = VersionControlRequirement
        fields = (
            'name',
            'vcs_type',
            'url'
        )
