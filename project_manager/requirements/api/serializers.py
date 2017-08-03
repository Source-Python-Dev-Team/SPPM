# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from ..models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class DownloadRequirementSerializer(ModelSerializer):
    class Meta:
        model = DownloadRequirement
        fields = (
            'name',
            'description',
            'url',
        )


class PyPiRequirementSerializer(ModelSerializer):
    class Meta:
        model = PyPiRequirement
        fields = (
            'name',
        )


class VersionControlRequirementSerializer(ModelSerializer):
    class Meta:
        model = VersionControlRequirement
        fields = (
            'name',
            'vcs_type',
            'url'
        )
