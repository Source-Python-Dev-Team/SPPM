"""Game API views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Count, F, Prefetch

# Third Party Django
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

# App
from games.api.serializers import GameListSerializer, GameRetrieveSerializer
from games.models import Game
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'GameViewSet',
)


# =============================================================================
# VIEWS
# =============================================================================
class GameViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """ViewSet for listing Supported Games.

    ###Available Ordering:

    *  **name** (descending) or **-name** (ascending)
    *  **basename** (descending) or **-basename** (ascending)
    *  **project_count** (descending) or **-project_count** (ascending)

        ####Example:
        `?ordering=name`

        `?ordering=-project_count`
    """

    filter_backends = (OrderingFilter,)
    queryset = Game.objects.all()
    ordering = ('name',)
    ordering_fields = ('basename', 'name', 'project_count')
    http_method_names = ('get', 'options')

    def retrieve(self, request, *args, **kwargs):
        """Overwrite the ordering fields on retrieve to exclude project_count.

        This helps avoid a FieldError since project_count is an annotation
            that only occurs during the list view.
        """
        self.ordering_fields = ('basename', 'name')
        return super().retrieve(request=request, *args, **kwargs)

    def get_serializer_class(self):
        """Return the correct serializer based on the action."""
        if self.action == 'retrieve':
            return GameRetrieveSerializer

        return GameListSerializer

    def get_queryset(self):
        """Filter the queryset to not return black-listed tags."""
        queryset = super().get_queryset()
        if self.action == 'retrieve':
            return queryset.prefetch_related(
                Prefetch(
                    lookup='sub_plugins',
                    queryset=SubPlugin.objects.select_related(
                        'plugin',
                    ).order_by(
                        'name',
                    ),
                ),
            )

        return queryset.annotate(
            package_count=Count('packages', distinct=True),
            plugin_count=Count('plugins', distinct=True),
            sub_plugin_count=Count('sub_plugins', distinct=True),
        ).annotate(
            project_count=F('package_count') + F('plugin_count') + F('sub_plugin_count'),
        )
