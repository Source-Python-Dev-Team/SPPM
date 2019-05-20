"""User serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

# App
from project_manager.packages.models import Package
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.models import SubPlugin
from project_manager.users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ForumUserSerializer',
    'PackageContributionSerializer',
    'PluginContributionSerializer',
    'ProjectContributionSerializer',
    'SubPluginContributionSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class ProjectContributionSerializer(ModelSerializer):
    """Base class for Project contributions."""

    class Meta:
        """Define metaclass attributes."""

        fields = (
            'name',
            'slug',
        )


class PackageContributionSerializer(ProjectContributionSerializer):
    """Serializer for Package Contributions."""

    class Meta(ProjectContributionSerializer.Meta):
        """Define metaclass attributes."""

        model = Package


class PluginContributionSerializer(ProjectContributionSerializer):
    """Serializer for Plugin Contributions."""

    class Meta(ProjectContributionSerializer.Meta):
        """Define metaclass attributes."""

        model = Plugin


class SubPluginContributionSerializer(ModelSerializer):
    """Serializer for SubPlugin Contributions."""

    plugin = PluginContributionSerializer()

    class Meta:
        """Define metaclass attributes."""

        model = SubPlugin
        fields = (
            'name',
            'slug',
            'plugin',
        )


class ForumUserSerializer(ModelSerializer):
    """Serializer for User Contributions."""

    username = SerializerMethodField()
    packages = PackageContributionSerializer(
        many=True,
        read_only=True,
    )
    package_contributions = PackageContributionSerializer(
        many=True,
        read_only=True,
    )
    plugins = PluginContributionSerializer(
        many=True,
        read_only=True,
    )
    plugin_contributions = PluginContributionSerializer(
        many=True,
        read_only=True,
    )
    subplugins = SubPluginContributionSerializer(
        many=True,
        read_only=True,
    )
    subplugin_contributions = SubPluginContributionSerializer(
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
            'subplugins',
            'subplugin_contributions',
        )

    @staticmethod
    def get_username(obj):
        """Return the user's username."""
        return obj.user.username
