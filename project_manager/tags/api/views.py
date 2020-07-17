"""Tag API views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

# App
from project_manager.tags.api.filtersets import TagFilterSet
from project_manager.tags.api.serializers import TagSerializer
from project_manager.tags.models import Tag


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'TagViewSet',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class TagViewSet(ListModelMixin, GenericViewSet):
    """ViewSet for listing Supported Games.

    ###Available Ordering:

    *  **name** (descending) or **-name** (ascending)
    *  **creator** (descending) or **-basename** (ascending)

        ####Example:
        `?ordering=name`

        `?ordering=-basename`
    """

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = TagFilterSet
    serializer_class = TagSerializer
    queryset = Tag.objects.select_related(
        'creator__user',
    )
    ordering = ('name',)
    ordering_fields = ('name',)
