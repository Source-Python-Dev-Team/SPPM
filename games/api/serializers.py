"""Game serializers for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

# App
from games.models import Game
from project_manager.packages.api.common.serializers import MinimalPackageSerializer
from project_manager.plugins.api.common.serializers import MinimalPluginSerializer
from project_manager.sub_plugins.api.common.serializers import MinimalSubPluginSerializer


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'GameListSerializer',
    'GameRetrieveSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class GameRetrieveSerializer(ModelSerializer):
    """Serializer for supported games for projects."""

    packages = MinimalPackageSerializer(many=True, read_only=True)
    plugins = MinimalPluginSerializer(many=True, read_only=True)
    subplugins = MinimalSubPluginSerializer(many=True, read_only=True)

    class Meta:
        """Define metaclass attributes."""

        model = Game
        fields = (
            'name',
            'slug',
            'icon',
            'packages',
            'plugins',
            'subplugins',
        )


class GameListSerializer(ModelSerializer):
    """Serializer for project Tags on list."""

    package_count = IntegerField()
    plugin_count = IntegerField()
    subplugin_count = IntegerField()
    project_count = IntegerField()

    class Meta:
        """Define metaclass attributes."""

        model = Game
        fields = (
            'name',
            'slug',
            'icon',
            'package_count',
            'plugin_count',
            'subplugin_count',
            'project_count',
        )
