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
# >> SERIALIZERS
# =============================================================================
class RequiredDownloadSerializer(ModelSerializer):
    class Meta:
        model = DownloadRequirement
        fields = (
            'name',
            'description',
            'url',
        )


class RequiredPyPiSerializer(ModelSerializer):
    class Meta:
        model = PyPiRequirement
        fields = (
            'name',
        )


class RequiredVersionControlSerializer(ModelSerializer):
    class Meta:
        model = VersionControlRequirement
        fields = (
            'name',
            'vcs_type',
            'url'
        )
