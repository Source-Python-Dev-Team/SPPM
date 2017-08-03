# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from ..models import Tag


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
        )
