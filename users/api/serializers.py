"""User serializers for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

# App
from project_manager.packages.api.common.serializers import MinimalPackageSerializer
from project_manager.plugins.api.common.serializers import MinimalPluginSerializer
from project_manager.sub_plugins.api.common.serializers import MinimalSubPluginSerializer
from users.models import ForumUser


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUserSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class ForumUserSerializer(ModelSerializer):
    """Serializer for User Contributions."""

    username = SerializerMethodField()
    packages = MinimalPackageSerializer(
        many=True,
        read_only=True,
    )
    package_contributions = MinimalPackageSerializer(
        many=True,
        read_only=True,
    )
    plugins = MinimalPluginSerializer(
        many=True,
        read_only=True,
    )
    plugin_contributions = MinimalPluginSerializer(
        many=True,
        read_only=True,
    )
    sub_plugins = MinimalSubPluginSerializer(
        many=True,
        read_only=True,
    )
    sub_plugin_contributions = MinimalSubPluginSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        """Define metaclass attributes."""

        model = ForumUser
        fields = (
            'forum_id',
            'username',
            'packages',
            'package_contributions',
            'plugins',
            'plugin_contributions',
            'sub_plugins',
            'sub_plugin_contributions',
        )

    @staticmethod
    def get_username(obj):
        """Return the user's username."""
        return obj.user.username
