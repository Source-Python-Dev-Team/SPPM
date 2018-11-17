"""Requirement API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
#  Django
from django.db.models import Prefetch

# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# App
from project_manager.packages.models import PackageRelease
from project_manager.plugins.models import PluginRelease
from project_manager.requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from project_manager.sub_plugins.models import SubPluginRelease
from .serializers import (
    DownloadRequirementSerializer,
    PyPiRequirementSerializer,
    VersionControlRequirementSerializer,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'DownloadRequirementViewSet',
    'PyPiRequirementViewSet',
    'RequirementAPIView',
    'VersionControlRequirementViewSet',
)


# =============================================================================
# >> GLOBALS
# =============================================================================
_project_prefetch = (
    Prefetch(
        lookup='required_in_package_releases',
        queryset=PackageRelease.objects.order_by(
            'package__name',
        )
    ),
    Prefetch(
        lookup='required_in_plugin_releases',
        queryset=PluginRelease.objects.order_by(
            'plugin__name',
        )
    ),
    Prefetch(
        lookup='required_in_sub_plugin_releases',
        queryset=SubPluginRelease.objects.order_by(
            'sub_plugin__name',
        ).select_related(
            'sub_plugin__plugin'
        )
    ),
)


# =============================================================================
# >> VIEWS
# =============================================================================
class RequirementAPIView(APIView):
    """Requirement API routes."""

    http_method_names = ('get', 'options')

    @staticmethod
    def get(request):
        """Return all API routes for requirements."""
        return Response(
            data={
                'download': reverse(
                    viewname='api:requirements:download-list',
                    request=request,
                ),
                'pypi': reverse(
                    viewname='api:requirements:pypi-list',
                    request=request,
                ),
                'vcs': reverse(
                    viewname='api:requirements:vcs-list',
                    request=request,
                ),
            }
        )

    def get_view_name(self):
        """Return the Requirement API name."""
        return 'Requirement APIs'


class DownloadRequirementViewSet(ModelViewSet):
    """ViewSet for getting and listing Download requirements."""

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering = ('name',)
    ordering_fields = ('name',)
    queryset = DownloadRequirement.objects.prefetch_related(
        *_project_prefetch,
    )
    http_method_names = ('get', 'options')
    lookup_field = 'name'
    serializer_class = DownloadRequirementSerializer


class PyPiRequirementViewSet(ModelViewSet):
    """ViewSet for getting and listing PyPi requirements."""

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering = ('name',)
    ordering_fields = ('name',)
    queryset = PyPiRequirement.objects.prefetch_related(
        *_project_prefetch,
    )
    http_method_names = ('get', 'options')
    lookup_field = 'name'
    serializer_class = PyPiRequirementSerializer


class VersionControlRequirementViewSet(ModelViewSet):
    """ViewSet for getting and listing Version Control requirements."""

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering = ('name',)
    ordering_fields = ('name',)
    queryset = VersionControlRequirement.objects.prefetch_related(
        *_project_prefetch,
    )
    http_method_names = ('get', 'options')
    lookup_field = 'name'
    serializer_class = VersionControlRequirementSerializer
