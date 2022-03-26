"""Tag serializers for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.relations import RelatedField
from rest_framework.serializers import ModelSerializer

# App
from tags.models import Tag
from users.api.serializers.common import ForumUserContributorSerializer


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'RelatedTagSerializer',
    'TagSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class RelatedTagSerializer(RelatedField):
    """Serializer for project tag fields."""

    def to_representation(self, value):
        """Return the name of the project."""
        return value.name


class TagSerializer(ModelSerializer):
    """Serializer for project Tags."""

    creator = ForumUserContributorSerializer(
        read_only=True,
    )
    packages = RelatedTagSerializer(many=True, read_only=True)
    plugins = RelatedTagSerializer(many=True, read_only=True)
    subplugins = RelatedTagSerializer(many=True, read_only=True)

    class Meta:
        """Define metaclass attributes."""

        model = Tag
        fields = (
            'name',
            'packages',
            'plugins',
            'subplugins',
            'creator',
        )
