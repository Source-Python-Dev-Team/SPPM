"""User serializers for APIs in other apps."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUserContributorSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class ForumUserContributorSerializer(ModelSerializer):
    """Used for owner/contributors for Projects."""

    class Meta:
        model = ForumUser
        fields = (
            'id',
            'username',
        )
