"""Plugin API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.reverse import reverse

# App
from project_manager.common.api.helpers import get_prefetch
from project_manager.common.api.views.mixins import ProjectThroughModelMixin
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectReleaseViewSet,
    ProjectTagViewSet,
    ProjectViewSet,
)
from .filters import PluginFilter
from .serializers import (
    PluginContributorSerializer,
    PluginCreateSerializer,
    PluginGameSerializer,
    PluginImageSerializer,
    PluginReleaseSerializer,
    PluginSerializer,
    PluginTagSerializer,
    SubPluginPathSerializer,
)
from ..models import (
    Plugin,
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginRelease,
    PluginTag,
    SubPluginPath,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginAPIView',
    'PluginContributorViewSet',
    'PluginGameViewSet',
    'PluginImageViewSet',
    'PluginReleaseViewSet',
    'PluginTagViewSet',
    'PluginViewSet',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PluginAPIView(ProjectAPIView):
    """Plugin API routes."""

    project_type = 'plugin'

    def get(self, request):
        response = super().get(request=request)
        response.data['paths'] = reverse(
            viewname=f'api:{self.project_type}s:endpoints',
            request=request,
        ) + f'paths/{self.extra_params}<{self.project_type}>/'
        return response


class PluginViewSet(ProjectViewSet):
    """ViewSet for creating, updating, and listing Plugins."""

    filter_class = PluginFilter
    queryset = Plugin.objects.prefetch_related(
        *get_prefetch(
            release_class=PluginRelease,
        )
    ).select_related(
        'owner__user',
    )
    serializer_class = PluginSerializer

    creation_serializer_class = PluginCreateSerializer


class PluginImageViewSet(ProjectImageViewSet):
    """ViewSet for adding, removing, and listing images for Plugins."""

    queryset = PluginImage.objects.select_related(
        'plugin',
    )
    serializer_class = PluginImageSerializer

    project_type = 'plugin'
    project_model = Plugin


class PluginReleaseViewSet(ProjectReleaseViewSet):
    """ViewSet for retrieving releases for Plugins."""

    queryset = PluginRelease.objects.select_related(
        'plugin',
    )
    serializer_class = PluginReleaseSerializer

    project_type = 'plugin'
    project_model = Plugin


class PluginGameViewSet(ProjectGameViewSet):
    """Supported Games listing for Plugins."""

    http_method_names = ('get', 'post', 'delete', 'options')
    queryset = PluginGame.objects.select_related(
        'game',
        'plugin',
    )
    serializer_class = PluginGameSerializer

    project_type = 'plugin'
    project_model = Plugin


class PluginTagViewSet(ProjectTagViewSet):
    """Tags listing for Plugins."""

    http_method_names = ('get', 'post', 'delete', 'options')
    queryset = PluginTag.objects.select_related(
        'tag',
        'plugin',
    )
    serializer_class = PluginTagSerializer

    project_type = 'plugin'
    project_model = Plugin


class PluginContributorViewSet(ProjectContributorViewSet):
    """Contributors listing for Plugins."""

    http_method_names = ('get', 'post', 'delete', 'options')
    queryset = PluginContributor.objects.select_related(
        'user__user',
        'plugin',
    )
    serializer_class = PluginContributorSerializer

    project_type = 'plugin'
    project_model = Plugin


class SubPluginPathViewSet(ProjectThroughModelMixin):
    """"""

    http_method_names = ('get', 'post', 'delete', 'options')
    ordering = ('path',)
    queryset = SubPluginPath.objects.select_related(
        'plugin',
    )
    serializer_class = SubPluginPathSerializer

    api_type = 'Sub-Plugin Paths'
    project_type = 'plugin'
    project_model = Plugin
