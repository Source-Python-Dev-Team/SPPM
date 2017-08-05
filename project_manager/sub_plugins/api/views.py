# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import ParseError
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# App
from .filters import PluginFilter
from .serializers import (
    SubPluginSerializer,
    SubPluginCreateSerializer,
    SubPluginUpdateSerializer,
)
from ..models import SubPlugin, SubPluginImage, SubPluginRelease
from project_manager.common.api.helpers import get_prefetch
from project_manager.plugins.models import Plugin


# =============================================================================
# >> VIEWS
# =============================================================================
class SubPluginAPIView(APIView):
    http_method_names = ('get', 'options')

    def get(self, request):
        return Response(
            data={
                'projects': reverse(
                    viewname='api:sub-plugins:endpoints',
                    request=request,
                ) + 'projects/<plugin>/',
            }
        )


class SubPluginViewSet(ModelViewSet):
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = PluginFilter
    ordering = ('-releases__created',)
    ordering_fields = ('name', 'basename', 'modified')
    queryset = SubPlugin.objects.prefetch_related(
        *get_prefetch(
            release_class=SubPluginRelease,
            image_class=SubPluginImage,
        )
    ).select_related(
        'owner',
        'plugin',
    )
    serializer_class = SubPluginSerializer
    lookup_field = 'slug'
    plugin = None

    def get_serializer_class(self):
        if self.action == 'update':
            return SubPluginUpdateSerializer
        if self.action == 'create':
            return SubPluginCreateSerializer
        if self.action == 'list':
            return self.serializer_class
        return self.serializer_class

    def get_queryset(self):
        print(self.args)
        print(self.kwargs)
        queryset = super().get_queryset()
        if self.plugin is not None:
            return queryset.filter(plugin=self.plugin)
        plugin_slug = self.kwargs.get('plugin_slug')
        try:
            self.plugin = Plugin.objects.get(slug=plugin_slug)
            return queryset.filter(plugin=self.plugin)
        except Plugin.DoesNotExist:
            raise ParseError('Invalid plugin_slug')
