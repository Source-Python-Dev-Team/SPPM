# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.exceptions import ParseError
from rest_framework.viewsets import ModelViewSet

# App
from .serializers import SubPluginSerializer
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# VIEWS
# =============================================================================
class SubPluginViewSet(ModelViewSet):

    queryset = SubPlugin.objects.all()
    serializer_class = SubPluginSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        plugin_slug = self.kwargs.get('plugin_slug')
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
            return queryset.filter(plugin=plugin)
        except Plugin.DoesNotExist:
            raise ParseError('Invalid plugin_slug')
