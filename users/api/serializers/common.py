"""User serializers for APIs in other apps."""

# =============================================================================
# IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

# App
from users.models import ForumUser


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUserContributorSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class ForumUserContributorSerializer(ModelSerializer):
    """Used for owner/contributors for Projects."""

    username = SerializerMethodField()

    class Meta:
        """Define metaclass attributes."""

        model = ForumUser
        fields = (
            'forum_id',
            'username',
        )

    @staticmethod
    def get_username(obj):
        """Return the user's username."""
        return obj.user.username
