"""Tag serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.tags.models import Tag
from project_manager.users.api.serializers.common import (
    ForumUserContributorSerializer,
)


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

    creator = ForumUserContributorSerializer(
        read_only=True,
    )

    class Meta:
        """Define metaclass attributes."""

        model = Tag
        fields = (
            'name',
            'black_listed',
            'creator',
        )
