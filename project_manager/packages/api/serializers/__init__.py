# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.common.api.serializers import (
    ProjectReleaseSerializer,
    ProjectSerializer,
)
from project_manager.packages.helpers import get_package_basename
from project_manager.packages.models import (
    Package,
    PackageImage,
    PackageRelease,
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
# TODO: APIs
# TODO:     contributors
# TODO:     images
# TODO:     supported_games
# TODO:     tags
class PackageImageSerializer(ModelSerializer):
    class Meta:
        model = PackageImage
        fields = (
            'image',
        )


class PackageReleaseSerializer(ProjectReleaseSerializer):
    project_class = Package
    project_type = 'package'
    zip_parser = get_package_basename

    class Meta(ProjectReleaseSerializer.Meta):
        model = PackageRelease


class PackageSerializer(ProjectSerializer):
    images = PackageImageSerializer(
        many=True,
        read_only=True,
    )
    releases = PackageReleaseSerializer(
        write_only=True,
    )

    project_type = 'package'
    release_model = PackageRelease

    class Meta(ProjectSerializer.Meta):
        model = Package
        fields = ProjectSerializer.Meta.fields + (
            'images',
            'releases',
        )
