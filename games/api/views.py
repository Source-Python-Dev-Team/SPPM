"""Game API views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

# App
from games.api.serializers import GameSerializer
from games.models import Game


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'GameViewSet',
)


# =============================================================================
# VIEWS
# =============================================================================
class GameViewSet(ListModelMixin, GenericViewSet):
    """ViewSet for listing Supported Games.

    ###Available Ordering:

    *  **name** (descending) or **-name** (ascending)
    *  **basename** (descending) or **-basename** (ascending)

        ####Example:
        `?ordering=name`

        `?ordering=-basename`
    """

    filter_backends = (OrderingFilter,)
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    ordering = ('name',)
    ordering_fields = ('basename', 'name')
    http_method_names = ('get', 'options')
