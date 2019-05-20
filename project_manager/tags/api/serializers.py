"""Tag serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.tags.models import Tag


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'TagSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class TagSerializer(ModelSerializer):
    """Serializer for project Tags."""

    class Meta:
        """Define metaclass attributes."""

        model = Tag
        fields = (
            'name',
        )
