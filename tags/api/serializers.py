"""Tag serializers for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.serializers import ModelSerializer

# App
from tags.models import Tag
from users.api.serializers.common import ForumUserContributorSerializer


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'TagSerializer',
)


# =============================================================================
# SERIALIZERS
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
