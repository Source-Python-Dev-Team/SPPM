# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
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
    class Meta:
        fields = (
            'name',
            'slug',
        )


class PackageContributionSerializer(ProjectContributionSerializer):
    class Meta(ProjectContributionSerializer.Meta):
        model = Package


class PluginContributionSerializer(ProjectContributionSerializer):
    class Meta(ProjectContributionSerializer.Meta):
        model = Plugin


class SubPluginContributionSerializer(ModelSerializer):
    plugin = PluginContributionSerializer()

    class Meta:
        model = SubPlugin
        fields = (
            'name',
            'slug',
            'plugin',
        )


class ForumUserSerializer(ModelSerializer):
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
        model = ForumUser
        fields = (
            'id',
            'username',
            'packages',
            'package_contributions',
            'plugins',
            'plugin_contributions',
            'subplugins',
            'subplugin_contributions',
        )
