# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class SubPluginSerializer(ModelSerializer):

    class Meta:
        model = SubPlugin
        fields = (
            'name', 'logo', 'description', 'configuration', 'owner',
            'contributors', 'download_requirements', 'package_requirements',
            'pypi_requirements', 'supported_games', 'synopsis',
            'get_forum_url',
        )
