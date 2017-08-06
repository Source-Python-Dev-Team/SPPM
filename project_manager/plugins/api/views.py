# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# App
from .filters import PluginFilter
from .serializers import PluginImageSerializer, PluginSerializer
from ..models import Plugin, PluginImage, PluginRelease
from project_manager.common.api.helpers import get_prefetch
from project_manager.common.api.views import ProjectImageViewSet


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
class PluginAPIView(APIView):
    http_method_names = ('get', 'options')

    def get(self, request):
        return Response(
            data={
                'projects': reverse(
                    viewname='api:plugins:projects-list',
                    request=request,
                ),
                'images': reverse(
                    viewname='api:plugins:endpoints',
                    request=request,
                ) + 'images/<plugin>/',
            }
        )


class PluginViewSet(ModelViewSet):
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
        'owner',
    )
    serializer_class = PluginSerializer


class PluginImageViewSet(ProjectImageViewSet):
    queryset = PluginImage.objects.select_related(
        'plugin',
    )
    serializer_class = PluginImageSerializer

    project_type = 'plugin'
    project_model = Plugin
