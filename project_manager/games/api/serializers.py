# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from ..models import Game


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GameSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'name',
            'slug',
            'icon',
        )
