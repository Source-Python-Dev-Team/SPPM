"""Package serializers for APIs in other apps."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.packages.models import Package


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageRequirementSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class PackageRequirementSerializer(ModelSerializer):
    """Serializer for Package requirements."""

    class Meta:
        model = Package
        fields = (
            'name',
            'slug',
        )
