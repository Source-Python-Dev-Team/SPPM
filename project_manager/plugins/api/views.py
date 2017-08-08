"""Plugin API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

# App
from project_manager.common.api.helpers import get_prefetch
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectImageViewSet,
    ProjectViewSet,
)
from .filters import PluginFilter
from .serializers import PluginImageSerializer, PluginSerializer
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

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = PluginFilter
    ordering = ('-releases__created',)
    ordering_fields = ('name', 'basename', 'modified')
    queryset = Plugin.objects.prefetch_related(
        *get_prefetch(
            release_class=PluginRelease,
            image_class=PluginImage,
        )
    ).select_related(
        'owner__user',
    )
    serializer_class = PluginSerializer


class PluginImageViewSet(ProjectImageViewSet):
    """ViewSet for adding, removing, and listing images for Plugins."""

    queryset = PluginImage.objects.select_related(
        'plugin',
    )
    serializer_class = PluginImageSerializer

    project_type = 'plugin'
    project_model = Plugin
