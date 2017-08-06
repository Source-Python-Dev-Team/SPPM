"""SubPlugin API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import ParseError
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# App
from project_manager.common.api.helpers import get_prefetch
from project_manager.common.api.views import ProjectImageViewSet
from project_manager.plugins.models import Plugin
from .filters import SubPluginFilter
from .serializers import SubPluginImageSerializer, SubPluginSerializer
from ..models import SubPlugin, SubPluginImage, SubPluginRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAPIView',
    'SubPluginImageViewSet',
    'SubPluginViewSet',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class SubPluginAPIView(APIView):
    """SubPlugin API routes."""

    http_method_names = ('get', 'options')

    @staticmethod
    def get(request):
        """Return all the API routes for SubPlugins."""
        return Response(
            data={
                'projects': reverse(
                    viewname='api:sub-plugins:endpoints',
                    request=request,
                ) + 'projects/<plugin>/',
                'images': reverse(
                    viewname='api:sub-plugins:endpoints',
                    request=request,
                ) + 'images/<plugin>/<sub-plugin>/',
            }
        )


class SubPluginViewSet(ModelViewSet):
    """ViewSet for creating, updating, and listing SubPlugins."""

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = SubPluginFilter
    ordering = ('-releases__created',)
    ordering_fields = ('name', 'basename', 'modified')
    queryset = SubPlugin.objects.prefetch_related(
        *get_prefetch(
            release_class=SubPluginRelease,
            image_class=SubPluginImage,
        )
    ).select_related(
        'owner',
        'plugin',
    )
    serializer_class = SubPluginSerializer
    lookup_field = 'slug'
    plugin = None

    def get_queryset(self):
        """Filter down to only SubPlugins for the given Plugin."""
        queryset = super().get_queryset()
        if self.plugin is not None:
            return queryset.filter(plugin=self.plugin)
        plugin_slug = self.kwargs.get('plugin_slug')
        try:
            self.plugin = Plugin.objects.get(slug=plugin_slug)
            return queryset.filter(plugin=self.plugin)
        except Plugin.DoesNotExist:
            raise ParseError('Invalid plugin_slug.')


class SubPluginImageViewSet(ProjectImageViewSet):
    """ViewSet for adding, removing, and listing images for SubPlugins."""

    queryset = SubPluginImage.objects.select_related(
        'sub_plugin',
    )
    serializer_class = SubPluginImageSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin

    @property
    def parent_project(self):
        """Return the Plugin for the SubPlugin image view."""
        plugin_slug = self.kwargs.get('plugin_slug')
        # TODO: figure out if this try/except is necessary
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
        except Plugin.DoesNotExist:
            raise ParseError(f'Plugin "{plugin_slug}" not found.')
        return plugin

    def get_project_kwargs(self, parent_project=None):
        """Add the Plugin to the kwargs for filtering for the project."""
        kwargs = super().get_project_kwargs(parent_project=parent_project)
        kwargs.update(
            plugin=parent_project,
        )
        return kwargs
