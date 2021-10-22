"""Game serializers for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from games.models import Game


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'GameSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class GameSerializer(ModelSerializer):
    """Serializer for supported games for projects."""

    class Meta:
        """Define metaclass attributes."""

        model = Game
        fields = (
            'name',
            'slug',
            'icon',
        )
