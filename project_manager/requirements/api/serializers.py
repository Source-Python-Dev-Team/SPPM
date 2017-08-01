# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

# App
from ..models import PyPiRequirement


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class PyPiRequirementSerializer(ModelSerializer):
    # pypi_url = SerializerMethodField()

    class Meta:
        model = PyPiRequirement
        fields = (
            'name',
            # 'pypi_url',
        )
