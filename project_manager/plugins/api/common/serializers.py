"""Plugin serializers for APIs in other apps."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.plugins.models import Plugin


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'MinimalPluginSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class MinimalPluginSerializer(ModelSerializer):
    """Serializer for Package Contributions."""

    class Meta:
        """Define metaclass attributes."""

        model = Plugin
        fields = (
            'name',
            'slug',
        )
