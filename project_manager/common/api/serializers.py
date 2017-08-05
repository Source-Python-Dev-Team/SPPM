# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.utils import formats
from django.utils.timezone import now

# 3rd-Party Django
from rest_framework.fields import CharField, FileField, SerializerMethodField
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

# App
from project_manager.games.api.serializers import GameSerializer
from project_manager.packages.api.serializers.common import (
    PackageRequirementSerializer
)
from project_manager.requirements.api.serializers.common import (
    RequiredDownloadSerializer,
    RequiredPyPiSerializer,
    RequiredVersionControlSerializer,
)
from project_manager.tags.api.serializers import TagSerializer
from project_manager.users.api.serializers.common import (
    ForumUserContributorSerializer,
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class ProjectSerializer(ModelSerializer):
    current_release = SerializerMethodField()
    owner = ForumUserContributorSerializer(
        read_only=True,
    )
    contributors = ForumUserContributorSerializer(
        many=True,
        read_only=True,
    )
    created = SerializerMethodField()
    updated = SerializerMethodField()
    package_requirements = PackageRequirementSerializer(
        many=True,
        read_only=True,
    )
    download_requirements = RequiredDownloadSerializer(
        many=True,
        read_only=True,
    )
    pypi_requirements = RequiredPyPiSerializer(
        many=True,
        read_only=True,
    )
    vcs_requirements = RequiredVersionControlSerializer(
        many=True,
        read_only=True,
    )
    supported_games = GameSerializer(
        many=True,
        read_only=True,
    )
    tags = TagSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        fields = (
            'name',
            'slug',
            'total_downloads',
            'current_release',
            'created',
            'updated',
            'synopsis',
            'description',
            'configuration',
            'logo',
            'owner',
            'contributors',
            'package_requirements',
            'download_requirements',
            'pypi_requirements',
            'vcs_requirements',
            'supported_games',
            'tags',
        )
        read_only_fields = (
            'slug',
        )

    @property
    def project_type(self):
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_type" attribute.'
        )

    @property
    def release_model(self):
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"release_model" attribute.'
        )

    def create(self, validated_data):
        release_dict = validated_data.pop('releases', {})
        version = release_dict['version']
        zip_file = release_dict['zip_file']
        notes = release_dict['notes']
        instance = super().create(validated_data)
        kwargs = {
            '{project_type}'.format(
                project_type=self.project_type.replace('-', '_')
            ): instance,
            'notes': notes,
            'version': version,
            'zip_file': zip_file,
        }
        self.release_model.objects.create(**kwargs)
        return instance

    def get_created(self, obj):
        return self.get_date_time_dict(timestamp=obj.created)

    def get_current_release(self, obj):
        try:
            release = obj.releases.all()[0]
        except IndexError:
            return {}
        zip_url = reverse(
            viewname=f'{self.project_type}-download',
            kwargs=self.get_download_kwargs(
                obj=obj,
                release=release,
            ),
            request=self.context['request']
        )
        return {
            'version': release.version,
            'notes': str(release.notes) if release.notes else release.notes,
            'zip_file': zip_url,
        }

    def get_date_time_dict(self, timestamp):
        return {
            'actual': timestamp,
            'locale': self.get_date_display(
                date=timestamp,
                date_format='DATE_FORMAT',
            ),
            'locale_short': self.get_date_display(
                date=timestamp,
                date_format='SHORT_DATE_FORMAT',
            )
        }

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        action = self.context['view'].action
        if action == 'update':
            name_kwargs = extra_kwargs.get('name', {})
            name_kwargs['read_only'] = True
            extra_kwargs['name'] = name_kwargs
        return extra_kwargs

    def get_updated(self, obj):
        return self.get_date_time_dict(timestamp=obj.modified)

    def update(self, instance, validated_data):
        release_dict = validated_data.pop('releases', {})
        version = release_dict.get('version', '')
        zip_file = release_dict.get('zip_file')
        if all([version, zip_file]):
            notes = release_dict.get('notes', '')
            kwargs = {
                '{project_type}'.format(
                    project_type=self.project_type.replace('-', '_')
                ): instance,
                'notes': notes,
                'version': version,
                'zip_file': zip_file,
            }
            self.release_model.objects.create(**kwargs)

        super().update(
            instance=instance,
            validated_data=validated_data,
        )

        return instance

    def validate(self, attrs):
        release_dict = attrs.get('releases', {})
        version = release_dict.get('version', '')
        zip_file = release_dict.get('zip_file')
        if not all([version, zip_file]):
            raise ValidationError({
                'releases': (
                    'Version and Zip File are required when creating a '
                    f'{self.project_type}.'
                )
            })

    @staticmethod
    def get_date_display(date, date_format):
        return formats.date_format(
            value=date,
            format=date_format,
        ) if date else date

    @staticmethod
    def get_download_kwargs(obj, release):
        return {
            'slug': obj.slug,
            'zip_file': release.file_name,
        }


class ProjectReleaseSerializer(ModelSerializer):
    notes = CharField(max_length=512, allow_blank=True)
    version = CharField(max_length=8, allow_blank=True)
    zip_file = FileField(allow_null=True)

    parent_project = None
    slug_kwarg = 'pk'

    class Meta:
        model = None
        fields = (
            'notes',
            'zip_file',
            'version',
        )

    @property
    def project_class(self):
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_class" attribute.'
        )

    @property
    def project_type(self):
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_type" attribute.'
        )

    @property
    def zip_parser(self):
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_class" attribute.'
        )

    def get_project_kwargs(self, parent_project=None):
        return {
            'pk': self.context['view'].kwargs.get('pk')
        }

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

        # Validate the version is new for the project
        parent_project = self.parent_project
        kwargs = self.get_project_kwargs(parent_project)
        try:
            project = self.project_class.objects.get(**kwargs)
            project_basename = project.basename
        except self.project_class.DoesNotExist:
            project_basename = None
        else:
            kwargs = {
                '{project_type}'.format(
                    project_type=self.project_type.replace('-', '_')
                ): project,
                'version': version,
            }
            if self.Meta.model.objects.filter(**kwargs).exists():
                raise ValidationError({
                    'version': 'Given version matches existing version.',
                })

        args = (zip_file,)
        if parent_project is not None:
            args += (parent_project,)
        basename = self.zip_parser(*args)
        if project_basename not in (basename, None):
            raise ValidationError({
                'zip_file': (
                    f"Basename in zip '{basename}' does not match basename "
                    f"for {self.project_type} '{project_basename}'"
                )
            })
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data=validated_data)
        getattr(instance, self.project_type.replace('-', '_')).update(
            modified=instance.created,
        )
        return instance


class ProjectImageSerializer(ModelSerializer):
    class Meta:
        fields = (
            'image',
        )

    def create(self, validated_data):
        view = self.context['view']
        validated_data[view.project_type.replace('-', '_')] = view.project
        return super().create(validated_data=validated_data)
