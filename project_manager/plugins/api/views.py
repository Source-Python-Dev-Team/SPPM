# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
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
from ..models import Plugin, PluginImage, PluginRelease
from project_manager.games.models import Game
from project_manager.packages.models import Package
from project_manager.requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from project_manager.tags.models import Tag
from project_manager.users.models import ForumUser


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
            ),
        ),
        Prefetch(
            lookup='contributors',
            queryset=ForumUser.objects.order_by(
                'username',
            ),
        ),
        Prefetch(
            lookup='package_requirements',
            queryset=Package.objects.order_by(
                'name',
            ),
        ),
        Prefetch(
            lookup='download_requirements',
            queryset=DownloadRequirement.objects.order_by(
                'name',
            ),
        ),
        Prefetch(
            lookup='pypi_requirements',
            queryset=PyPiRequirement.objects.order_by(
                'name',
            ),
        ),
        Prefetch(
            lookup='vcs_requirements',
            queryset=VersionControlRequirement.objects.order_by(
                'name',
            ),
        ),
        Prefetch(
            lookup='supported_games',
            queryset=Game.objects.order_by(
                'name',
            ),
        ),
        Prefetch(
            lookup='images',
            queryset=PluginImage.objects.order_by(
                'image',
            ),
        ),
        Prefetch(
            lookup='tags',
            queryset=Tag.objects.order_by(
                'name',
            ),
        ),
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
