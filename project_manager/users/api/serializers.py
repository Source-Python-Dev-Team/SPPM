# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from ..models import ForumUser


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class ForumUserSerializer(ModelSerializer):
    class Meta:
        model = ForumUser
        fields = (
            'id',
            'username',
        )
