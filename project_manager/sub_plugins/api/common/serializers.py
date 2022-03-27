"""SubPlugin serializers for APIs in other apps."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.plugins.api.common.serializers import MinimalPluginSerializer
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'MinimalSubPluginSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class MinimalSubPluginSerializer(ModelSerializer):
    """Serializer for SubPlugin Contributions."""

    plugin = MinimalPluginSerializer()

    class Meta:
        """Define metaclass attributes."""

        model = SubPlugin
        fields = (
            'name',
            'slug',
            'plugin',
        )
