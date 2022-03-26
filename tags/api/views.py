"""Tag API views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Prefetch

# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

# App
from project_manager.packages.models import Package
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.models import SubPlugin
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

    ###Available Ordering:

    *  **name** (descending) or **-name** (ascending)

        ####Example:
        `?ordering=name`

        `?ordering=-name`
    """

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    ordering = ('name',)
    ordering_fields = ('name',)
    http_method_names = ('get', 'options')

    def get_queryset(self):
        """Filter the queryset to not return black-listed tags."""
        return super().get_queryset().filter(
            black_listed=False,
        ).select_related(
            'creator__user',
        ).prefetch_related(
            Prefetch(
                lookup='packages',
                queryset=Package.objects.order_by('name'),
            ),
            Prefetch(
                lookup='plugins',
                queryset=Plugin.objects.order_by('name'),
            ),
            Prefetch(
                lookup='subplugins',
                queryset=SubPlugin.objects.order_by('name'),
            ),
        )
