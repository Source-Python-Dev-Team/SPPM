# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

# App
from .filters import PackageFilter
from .serializers import (
    PackageSerializer,
    PackageCreateSerializer,
    PackageUpdateSerializer,
)
from ..models import Package, PackageImage, PackageRelease
from project_manager.common.api.helpers import get_prefetch


# =============================================================================
# >> VIEWS
# =============================================================================
class PackageViewSet(ModelViewSet):
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = PackageFilter
    ordering = ('-releases__created',)
    ordering_fields = ('name', 'basename', 'modified')
    queryset = Package.objects.prefetch_related(
        *get_prefetch(
            release_class=PackageRelease,
            image_class=PackageImage,
        )
    ).select_related(
        'owner',
    )
    serializer_class = PackageSerializer

    def get_serializer_class(self):
        if self.action == 'update':
            return PackageUpdateSerializer
        if self.action == 'create':
            return PackageCreateSerializer
        if self.action == 'list':
            return self.serializer_class
        return self.serializer_class
