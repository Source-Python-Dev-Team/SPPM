# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.db.models import Prefetch

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
from ..models import Plugin, PluginRelease


# =============================================================================
# VIEWS
# =============================================================================
class PluginViewSet(ModelViewSet):
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = PluginFilter
    ordering = ('-releases__created', )
    ordering_fields = ('name', 'basename', 'modified')
    queryset = Plugin.objects.prefetch_related(
        Prefetch(
            lookup='releases',
            queryset=PluginRelease.objects.order_by(
                '-created',
            )
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
