# =============================================================================
# >> IMPORTS
# =============================================================================
#  Django
from django.db.models import Prefetch

# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

# App
from .serializers import (
    DownloadRequirementSerializer,
    PyPiRequirementSerializer,
    VersionControlRequirementSerializer,
)
from project_manager.packages.models import Package
from project_manager.plugins.models import Plugin
from project_manager.requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# >> GLOBALS
# =============================================================================
project_prefetch = (
    Prefetch(
        lookup='required_in_packages',
        queryset=Package.objects.order_by(
            'name',
        )
    ),
    Prefetch(
        lookup='required_in_plugins',
        queryset=Plugin.objects.order_by(
            'name',
        )
    ),
    Prefetch(
        lookup='required_in_subplugins',
        queryset=SubPlugin.objects.order_by(
            'name',
        ).select_related(
            'plugin'
        )
    ),
)


# =============================================================================
# >> VIEWS
# =============================================================================
class DownloadRequirementViewSet(ModelViewSet):
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering = ('name',)
    ordering_fields = ('name',)
    queryset = DownloadRequirement.objects.prefetch_related(
        *project_prefetch,
    )
    http_method_names = ('get', 'options')
    lookup_field = 'name'
    serializer_class = DownloadRequirementSerializer


class PyPiRequirementViewSet(ModelViewSet):
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering = ('name',)
    ordering_fields = ('name',)
    queryset = PyPiRequirement.objects.prefetch_related(
        *project_prefetch,
    )
    http_method_names = ('get', 'options')
    lookup_field = 'name'
    serializer_class = PyPiRequirementSerializer


class VersionControlRequirementViewSet(ModelViewSet):
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering = ('name',)
    ordering_fields = ('name',)
    queryset = VersionControlRequirement.objects.prefetch_related(
        *project_prefetch,
    )
    http_method_names = ('get', 'options')
    lookup_field = 'name'
    serializer_class = VersionControlRequirementSerializer
