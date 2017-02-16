# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.urlresolvers import reverse

# 3rd-Party Django
from rest_framework.viewsets import ModelViewSet

# App
from .serializers import PluginListSerializer, PluginSerializer
from project_manager.plugins.models import Plugin


# =============================================================================
# VIEWS
# =============================================================================
class PluginViewSet(ModelViewSet):

    queryset = Plugin.objects.all()
    serializer_class = PluginSerializer

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('releases')
        if self.action == 'list' and 'game' in self.request.query_params:
            queryset = queryset.filter(
                supported_games__basename__exact=(
                    self.request.query_params['game']
                )
            )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return PluginListSerializer
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        self.get_current_release(response.data)
        return response

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for data in response.data['results']:
            data['link'] = request.build_absolute_uri(
                reverse(
                    'plugins:detail',
                    args=(data['slug'], ),
                )
            )
            self.get_current_release(data)
        return response

    @staticmethod
    def get_current_release(data):
        count = len(data.get('releases', {}))
        if not count:
            data['current_release'] = None
            return
        if count == 1:
            data['current_release'] = data['releases'][0]
        else:
            newest_datetime = max([y['created'] for y in data['releases']])
            data['current_release'] = {
                y['created']: y for y in data['releases']
            }.get(newest_datetime)
        del data['releases']
