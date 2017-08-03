# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

# App
from .filters import PluginFilter
from .serializers import (
    PluginSerializer,
    PluginCreateSerializer,
    PluginUpdateSerializer,
)
from ..models import Plugin, PluginImage, PluginRelease
from project_manager.common.api.helpers import get_prefetch


# =============================================================================
# VIEWS
# =============================================================================
class PluginViewSet(ModelViewSet):
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = PluginFilter
    ordering = ('-releases__created', )
    ordering_fields = ('name', 'basename', 'modified')
    queryset = Plugin.objects.prefetch_related(
        *get_prefetch(
            release_class=PluginRelease,
            image_class=PluginImage,
        )
    ).select_related(
        'owner',
    )
    serializer_class = PluginSerializer

    def get_serializer_class(self):
        if self.action == 'update':
            return PluginUpdateSerializer
        if self.action == 'create':
            return PluginCreateSerializer
        if self.action == 'list':
            return self.serializer_class
        return self.serializer_class
