"""Game serializers for APIs in other apps."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.serializers import ModelSerializer

# App
from games.models import Game


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'MinimalGameSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class MinimalGameSerializer(ModelSerializer):
    """Serializer for Package Contributions."""

    class Meta:
        """Define metaclass attributes."""

        model = Game
        fields = (
            'name',
            'slug',
            'icon',
        )
