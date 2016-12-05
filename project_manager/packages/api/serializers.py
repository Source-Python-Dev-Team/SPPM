# =============================================================================
# >> IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.packages.models import Package


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class PackageSerializer(ModelSerializer):

    class Meta:
        model = Package
        fields = (
            'name', 'logo', 'description',
        )
