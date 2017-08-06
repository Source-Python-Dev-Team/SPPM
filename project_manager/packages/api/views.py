"""Package API views."""

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
from project_manager.common.api.helpers import get_prefetch
from project_manager.common.api.views import ProjectImageViewSet
from .filters import PackageFilter
from .serializers import PackageImageSerializer, PackageSerializer
from ..models import Package, PackageImage, PackageRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAPIView',
    'PackageImageViewSet',
    'PackageViewSet',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PackageAPIView(APIView):
    """Package API routes."""

    http_method_names = ('get', 'options')

    @staticmethod
    def get(request):
        """Return all the API routes for Packages."""
        return Response(
            data={
                'projects': reverse(
                    viewname='api:packages:projects-list',
                    request=request,
                ),
                'images': reverse(
                    viewname='api:packages:endpoints',
                    request=request,
                ) + 'images/<package>/',
            }
        )


class PackageViewSet(ModelViewSet):
    """ViewSet for creating, updating, and listing Packages."""

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


class PackageImageViewSet(ProjectImageViewSet):
    """ViewSet for adding, removing, and listing images for Packages."""

    queryset = PackageImage.objects.select_related(
        'package',
    )
    serializer_class = PackageImageSerializer

    project_type = 'package'
    project_model = Package
