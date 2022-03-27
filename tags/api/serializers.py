"""Tag serializers for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

# App
from project_manager.packages.api.common.serializers import MinimalPackageSerializer
from project_manager.plugins.api.common.serializers import MinimalPluginSerializer
from project_manager.sub_plugins.api.common.serializers import MinimalSubPluginSerializer
from tags.models import Tag


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'TagListSerializer',
    'TagRetrieveSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class TagRetrieveSerializer(ModelSerializer):
    """Serializer for project Tags on retrieve."""

    packages = MinimalPackageSerializer(many=True, read_only=True)
    plugins = MinimalPluginSerializer(many=True, read_only=True)
    sub_plugins = MinimalSubPluginSerializer(many=True, read_only=True)

    class Meta:
        """Define metaclass attributes."""

        model = Tag
        fields = (
            'name',
            'packages',
            'plugins',
            'sub_plugins',
        )


class TagListSerializer(ModelSerializer):
    """Serializer for project Tags on list."""

    package_count = IntegerField()
    plugin_count = IntegerField()
    sub_plugin_count = IntegerField()
    project_count = IntegerField()

    class Meta:
        """Define metaclass attributes."""

        model = Tag
        fields = (
            'name',
            'package_count',
            'plugin_count',
            'sub_plugin_count',
            'project_count',
        )
