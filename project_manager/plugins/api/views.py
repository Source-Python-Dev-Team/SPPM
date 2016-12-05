# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.viewsets import ModelViewSet

# App
from .serializers import PluginSerializer
from project_manager.plugins.models import Plugin


# =============================================================================
# VIEWS
# =============================================================================
class PluginViewSet(ModelViewSet):
    """Displays all available versions for the CPD API."""

    queryset = Plugin.objects.all()
    serializer_class = PluginSerializer
