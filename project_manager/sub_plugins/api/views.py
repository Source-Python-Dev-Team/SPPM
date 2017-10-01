"""SubPlugin API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from rest_framework.parsers import ParseError

# App
from project_manager.common.api.helpers import get_prefetch
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectReleaseViewSet,
    ProjectTagViewSet,
    ProjectViewSet,
)
from project_manager.plugins.models import Plugin
from .filters import SubPluginFilter
from .serializers import (
    SubPluginContributorSerializer,
    SubPluginCreateSerializer,
    SubPluginGameSerializer,
    SubPluginImageSerializer,
    SubPluginReleaseSerializer,
    SubPluginSerializer,
    SubPluginTagSerializer,
)
from ..models import (
    SubPlugin,
    SubPluginContributor,
    SubPluginGame,
    SubPluginImage,
    SubPluginRelease,
    SubPluginTag,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAPIView',
    'SubPluginContributorViewSet',
    'SubPluginGameViewSet',
    'SubPluginImageViewSet',
    'SubPluginReleaseViewSet',
    'SubPluginTagViewSet',
    'SubPluginViewSet',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class SubPluginAPIView(ProjectAPIView):
    """SubPlugin API routes."""

    project_type = 'sub-plugin'
    extra_params = '<plugin>/'


class SubPluginViewSet(ProjectViewSet):
    """ViewSet for creating, updating, and listing SubPlugins."""

    filter_class = SubPluginFilter
    queryset = SubPlugin.objects.prefetch_related(
        *get_prefetch(
            release_class=SubPluginRelease,
        )
    ).select_related(
        'owner__user',
        'plugin',
    )
    serializer_class = SubPluginSerializer
    lookup_field = 'slug'

    creation_serializer_class = SubPluginCreateSerializer
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
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
        except Plugin.DoesNotExist:
            raise ParseError(f"Plugin '{plugin_slug}' not found.")
        return plugin

    def get_project_kwargs(self, parent_project=None):
        """Add the Plugin to the kwargs for filtering for the project."""
        kwargs = super().get_project_kwargs(parent_project=parent_project)
        kwargs.update(
            plugin=parent_project,
        )
        return kwargs


class SubPluginReleaseViewSet(ProjectReleaseViewSet):
    """ViewSet for retrieving releases for SubPlugins."""

    queryset = SubPluginRelease.objects.select_related(
        'sub_plugin',
    )
    serializer_class = SubPluginReleaseSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin

    @property
    def parent_project(self):
        """Return the Plugin for the SubPlugin image view."""
        plugin_slug = self.kwargs.get('plugin_slug')
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
        except Plugin.DoesNotExist:
            raise ParseError(f"Plugin '{plugin_slug}' not found.")
        return plugin

    def get_project_kwargs(self, parent_project=None):
        """Add the Plugin to the kwargs for filtering for the project."""
        kwargs = super().get_project_kwargs(parent_project=parent_project)
        kwargs.update(
            plugin=parent_project,
        )
        return kwargs


class SubPluginGameViewSet(ProjectGameViewSet):
    """Supported Games listing for SubPlugins."""

    http_method_names = ('get', 'post', 'delete', 'options')
    queryset = SubPluginGame.objects.select_related(
        'game',
        'sub_plugin',
    )
    serializer_class = SubPluginGameSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin


class SubPluginTagViewSet(ProjectTagViewSet):
    """Tags listing for SubPlugins."""

    http_method_names = ('get', 'post', 'delete', 'options')
    queryset = SubPluginTag.objects.select_related(
        'tag',
        'sub_plugin',
    )
    serializer_class = SubPluginTagSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin


class SubPluginContributorViewSet(ProjectContributorViewSet):
    """Contributors listing for SubPlugins."""

    http_method_names = ('get', 'post', 'delete', 'options')
    queryset = SubPluginContributor.objects.select_related(
        'user__user',
        'sub_plugin',
    )
    serializer_class = SubPluginContributorSerializer

    project_type = 'sub-plugin'
    project_model = SubPlugin
