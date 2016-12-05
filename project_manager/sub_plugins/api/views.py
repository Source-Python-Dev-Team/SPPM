# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.viewsets import ModelViewSet

# App
from .serializers import SubPluginSerializer
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# VIEWS
# =============================================================================
class SubPluginViewSet(ModelViewSet):
    """Displays all available versions for the CPD API."""

    queryset = SubPlugin.objects.all()
    serializer_class = SubPluginSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.request.query_params.get('plugin')
        if slug is None:
            return queryset
        try:
            plugin = Plugin.objects.get(slug=slug)
        except Plugin.DoesNotExist:
            # TODO: Raise an error here
            return queryset
        return queryset.filter(plugin=plugin)
