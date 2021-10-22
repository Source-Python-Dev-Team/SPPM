"""Tag API views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

# App
from tags.api.filtersets import TagFilterSet
from tags.api.serializers import TagSerializer
from tags.models import Tag


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'TagViewSet',
)


# =============================================================================
# VIEWS
# =============================================================================
class TagViewSet(ListModelMixin, GenericViewSet):
    """ViewSet for listing Supported Games.

    ###Available Filters:
    *  **black_listed**=*{boolean}*
        * Filters on blacklisted or not blacklisted.

        ####Example:
        `?game=true`

        `?game=false`

    ###Available Ordering:

    *  **name** (descending) or **-name** (ascending)

        ####Example:
        `?ordering=name`

        `?ordering=-name`
    """

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = TagFilterSet
    serializer_class = TagSerializer
    queryset = Tag.objects.select_related(
        'creator__user',
    )
    ordering = ('name',)
    ordering_fields = ('name',)
