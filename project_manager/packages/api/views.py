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
from .filters import PackageFilter
from .serializers import PackageImageSerializer, PackageSerializer
from ..models import Package, PackageImage, PackageRelease
from project_manager.common.api.helpers import get_prefetch
from project_manager.common.api.views import ProjectImageViewSet


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
    http_method_names = ('get', 'options')

    def get(self, request):
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
    queryset = PackageImage.objects.select_related(
        'package',
    )
    serializer_class = PackageImageSerializer

    project_type = 'package'
    project_model = Package
