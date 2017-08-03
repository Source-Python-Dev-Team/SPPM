# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.packages.models import Package


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class PackageRequirementSerializer(ModelSerializer):
    class Meta:
        model = Package
        fields = (
            'name',
            'slug',
        )
