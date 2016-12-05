# =============================================================================
# >> IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.plugins.models import Plugin


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class PluginSerializer(ModelSerializer):

    class Meta:
        model = Plugin
        fields = (
            'name', 'logo', 'description',
        )
