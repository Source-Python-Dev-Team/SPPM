"""Plugin API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.helpers import get_prefetch
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectImageViewSet,
    ProjectReleaseViewSet,
    ProjectViewSet,
)
from .filters import PluginFilter
from .serializers import (
    PluginCreateSerializer,
    PluginImageSerializer,
    PluginReleaseListSerializer,
    PluginSerializer,
)
from ..models import Plugin, PluginImage, PluginRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginAPIView',
    'PluginImageViewSet',
    'PluginViewSet',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PluginAPIView(ProjectAPIView):
    """Plugin API routes."""

    project_type = 'plugin'


class PluginViewSet(ProjectViewSet):
    """ViewSet for creating, updating, and listing Plugins."""

    filter_class = PluginFilter
    queryset = Plugin.objects.prefetch_related(
        *get_prefetch(
            release_class=PluginRelease,
            image_class=PluginImage,
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
    serializer_class = PluginReleaseListSerializer

    project_type = 'plugin'
    project_model = Plugin
