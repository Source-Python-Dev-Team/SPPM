"""Package serializers for APIs in other apps."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

# App
from project_manager.packages.models import Package


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'MinimalPackageSerializer',
    'ReleasePackageRequirementSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class ReleasePackageRequirementSerializer(ModelSerializer):
    """Serializer for Package requirements."""

    name = ReadOnlyField(source='package_requirement.name')
    slug = ReadOnlyField(source='package_requirement.slug')
    version = ReadOnlyField()

    class Meta:
        """Define metaclass attributes."""

        fields = (
            'name',
            'slug',
            'version',
            'optional',
        )


class MinimalPackageSerializer(ModelSerializer):
    """Serializer for Package Contributions."""

    class Meta:
        """Define metaclass attributes."""

        model = Package
        fields = (
            'name',
            'slug',
        )
