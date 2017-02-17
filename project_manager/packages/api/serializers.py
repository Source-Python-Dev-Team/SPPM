# =============================================================================
# >> IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.serializers import ModelSerializer

# App
from project_manager.packages.models import Package, PackageRelease


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class PackageReleaseSerializer(ModelSerializer):

    class Meta:
        model = PackageRelease
        fields = (
            'version', 'notes', 'zip_file', 'created', 'modified',
        )


class PackageListSerializer(ModelSerializer):
    releases = PackageReleaseSerializer(many=True)

    class Meta:
        model = Package
        fields = (
            'name', 'slug', 'logo', 'synopsis', 'releases',
        )
        read_only_fields = ('slug', )


class PackageSerializer(PackageListSerializer):
    class Meta(PackageListSerializer.Meta):
        fields = PackageListSerializer.Meta.fields + (
            'description',
        )
