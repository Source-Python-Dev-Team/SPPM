# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.viewsets import ModelViewSet

# App
from .serializers import PackageSerializer
from project_manager.packages.models import Package


# =============================================================================
# VIEWS
# =============================================================================
class PackageViewSet(ModelViewSet):

    queryset = Package.objects.all()
    serializer_class = PackageSerializer
