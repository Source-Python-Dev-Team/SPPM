# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# 3rd-Party Django
from rest_framework.fields import CharField, FileField
from rest_framework.serializers import ModelSerializer

# App
from project_manager.common.api.mixins import ProjectSerializer
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
# TODO:     paths
# TODO:     supported_games
# TODO:     tags
class PackageImageSerializer(ModelSerializer):
    class Meta:
        model = PackageImage
        fields = (
            'image',
        )


class PackageSerializer(ProjectSerializer):
    reverse_path = 'package'

    images = PackageImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta(ProjectSerializer.Meta):
        model = Package
        fields = ProjectSerializer.Meta.fields + (
            'images',
        )


class PackageReleaseSerializer(ModelSerializer):
    notes = CharField(max_length=512, allow_blank=True)
    version = CharField(max_length=8, allow_blank=True)
    zip_file = FileField(allow_null=True)

    class Meta:
        model = PackageRelease
        fields = (
            'notes',
            'zip_file',
            'version',
        )

    def validate(self, attrs):
        version = attrs.get('version', '')
        zip_file = attrs.get('zip_file')
        if any([version, zip_file]) and not all([version, zip_file]):
            raise ValidationError({
                '__all__': (
                    "If either 'version' or 'zip_file' are provided, "
                    "must be provided."
                )
            })

        # Validate the version is new for the package
        try:
            package = Package.objects.get(pk=self.context['view'].kwargs['pk'])
            package_basename = package.basename
        except Package.DoesNotExist:
            package_basename = None
        else:
            if PackageRelease.objects.filter(
                package=package,
                version=version,
            ).exists():
                raise ValidationError({
                    'version': 'Given version matches existing version.',
                })

        basename = get_package_basename(zip_file)
        if basename != package_basename:
            raise ValidationError({
                'zip_file': (
                    f"Basename in zip '{basename}' does not match basename "
                    f"for package '{package_basename}'"
                )
            })
        return attrs


class PackageCreateSerializer(PackageSerializer):
    releases = PackageReleaseSerializer(write_only=True)

    class Meta(PackageSerializer.Meta):
        fields = PackageSerializer.Meta.fields + ('releases', )
        read_only_fields = PackageSerializer.Meta.read_only_fields

    def validate(self, attrs):
        release_dict = attrs.get('releases', {})
        version = release_dict.get('version', '')
        zip_file = release_dict.get('zip_file')
        if not all([version, zip_file]):
            raise ValidationError({
                'releases': (
                    'Version and Zip File are required when creating '
                    'a package.'
                )
            })

    def create(self, validated_data):
        release_dict = validated_data.pop('releases', {})
        version = release_dict['version']
        zip_file = release_dict['zip_file']
        notes = release_dict['notes']
        instance = super().create(validated_data)
        PackageRelease.objects.create(
            package=instance,
            notes=notes,
            version=version,
            zip_file=zip_file,
        )
        return instance


class PackageUpdateSerializer(PackageCreateSerializer):

    class Meta(PackageCreateSerializer.Meta):
        read_only_fields = PackageCreateSerializer.Meta.read_only_fields + (
            'name',
        )

    def update(self, instance, validated_data):
        release_dict = validated_data.pop('releases', {})
        version = release_dict.get('version', '')
        zip_file = release_dict.get('zip_file')
        if all([version, zip_file]):
            notes = release_dict.get('notes', '')
            PackageRelease.objects.create(
                package=instance,
                notes=notes,
                version=version,
                zip_file=zip_file,
            )

        super().update(
            instance=instance,
            validated_data=validated_data,
        )

        return instance
