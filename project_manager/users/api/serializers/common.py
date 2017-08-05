# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.users.models import ForumUser


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class ForumUserContributorSerializer(ModelSerializer):
    class Meta:
        model = ForumUser
        fields = (
            'id',
            'username',
        )
