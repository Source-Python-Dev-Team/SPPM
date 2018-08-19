"""Package serializers for APIs in other apps."""

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
    'ReleasePackageRequirementSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class ReleasePackageRequirementSerializer(ModelSerializer):
    """Serializer for Package requirements."""

    name = ReadOnlyField(source='package_requirement.name')
    slug = ReadOnlyField(source='package_requirement.slug')
    version = ReadOnlyField()

    class Meta:
        fields = (
            'name',
            'slug',
            'version',
            'optional',
        )
