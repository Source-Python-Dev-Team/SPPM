"""Common serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from operator import itemgetter

# Django
from django.core.exceptions import ValidationError
from django.utils.text import slugify

# 3rd-Party Django
from rest_framework.fields import CharField, FileField, SerializerMethodField
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

# App
from project_manager.games.api.serializers import GameSerializer
from project_manager.games.models import Game
from project_manager.packages.api.serializers.common import (
    PackageRequirementSerializer
)
from project_manager.requirements.api.serializers.common import (
    RequiredDownloadSerializer,
    RequiredPyPiSerializer,
    RequiredVersionControlSerializer,
)
from project_manager.tags.api.serializers import TagSerializer
from project_manager.tags.models import Tag
from project_manager.users.api.serializers.common import (
    ForumUserContributorSerializer,
)
from project_manager.users.models import ForumUser
from .mixins import ProjectLocaleMixin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectImageSerializer',
    'ProjectReleaseSerializer',
    'ProjectSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
# TODO: APIs for adding/removing
# TODO:     contributors
# TODO:     supported_games
# TODO:     tags
class ProjectSerializer(ModelSerializer, ProjectLocaleMixin):
    """Base Project Serializer."""

    current_release = SerializerMethodField()
    owner = ForumUserContributorSerializer(
        read_only=True,
    )
    contributors = ForumUserContributorSerializer(
        many=True,
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
    )
    tags = TagSerializer(
        many=True,
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
        """Return the project's type."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_type" attribute.'
        )

    @property
    def release_model(self):
        """Return the model to use for releases."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"release_model" attribute.'
        )

    def create(self, validated_data):
        """Create the instance and the first release of the project."""
        release_dict = validated_data.pop('releases')
        instance = super().create(validated_data)
        version = release_dict['version']
        zip_file = release_dict['zip_file']
        notes = release_dict['notes']
        instance.basename = release_dict['basename']
        instance.owner = self.context['request'].user.forum_user
        instance.slug = slugify(instance.basename)
        instance.save()
        kwargs = {
            '{project_type}'.format(
                project_type=self.project_type.replace('-', '_')
            ): instance,
            'notes': notes,
            'version': version,
            'zip_file': zip_file,
        }
        self.release_model.objects.create(**kwargs)
        self.update_all_many_to_many_fields(instance=instance)
        return instance

    def get_created(self, obj):
        """Return the project's created info."""
        return self.get_date_time_dict(timestamp=obj.created)

    def get_current_release(self, obj):
        """Return the current release info."""
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

    def get_extra_kwargs(self):
        """Set the 'name' field to read-only when updating."""
        extra_kwargs = super().get_extra_kwargs()
        action = self.context['view'].action
        if action == 'update':
            name_kwargs = extra_kwargs.get('name', {})
            name_kwargs['read_only'] = True
            extra_kwargs['name'] = name_kwargs
        return extra_kwargs

    def get_updated(self, obj):
        """Return the project's last updated info."""
        return self.get_date_time_dict(timestamp=obj.modified)

    def update(self, instance, validated_data):
        """Update the project."""
        super().update(
            instance=instance,
            validated_data=validated_data,
        )
        self.update_all_many_to_many_fields(instance=instance)
        return instance

    def update_all_many_to_many_fields(self, instance):
        """Update the many-to-many fields with the given values."""
        self.update_many_to_many(
            instance=instance,
            field_name='contributors',
            related_model=ForumUser,
            related_field_name='forum_id',
        )
        self.update_many_to_many(
            instance=instance,
            field_name='supported_games',
            related_model=Game,
            related_field_name='slug',
        )
        # TODO: add any new tags
        # TODO: create a blacklist for tag names that can be handled via admin
        self.update_many_to_many(
            instance=instance,
            field_name='tags',
            related_model=Tag,
            related_field_name='name',
        )

    def update_many_to_many(
        self, instance, field_name, related_model, related_field_name
    ):
        """Update the given many-to-many."""
        stored_object = getattr(self.context['view'], f'stored_{field_name}')

        # If patching, there might be nothing passed
        if stored_object is None:
            return

        kwargs = {
            f'{related_field_name}__in': map(
                itemgetter(related_field_name),
                stored_object,
            )
        }
        stored_values = related_model.objects.filter(**kwargs).in_bulk()
        related_queryset = getattr(instance, field_name)
        current_values = related_queryset.in_bulk()

        values_to_remove = set(current_values).difference(
            stored_values,
        )
        values_to_add = set(stored_values).difference(
            current_values,
        )

        related_queryset.remove(
            *[current_values[x] for x in values_to_remove]
        )
        related_queryset.add(
            *[stored_values[x] for x in values_to_add]
        )

    def validate(self, attrs):
        """Validate the given field values."""
        release_dict = attrs.get('releases', {})
        version = release_dict.get('version', '')
        zip_file = release_dict.get('zip_file')
        if (
            self.context['request'].method == 'POST' and
            not all([version, zip_file])
        ):
            raise ValidationError({
                'releases': (
                    'Version and Zip File are required when using POST or PUT '
                    f'for creating/updating a {self.project_type}.'
                )
            })
        return attrs

    @staticmethod
    def get_download_kwargs(obj, release):
        """Return the release's reverse kwargs."""
        return {
            'slug': obj.slug,
            'zip_file': release.file_name,
        }


class ProjectReleaseListSerializer(ModelSerializer, ProjectLocaleMixin):
    """Base ProjectRelease Serializer for listing."""

    created = SerializerMethodField()

    class Meta:
        model = None
        fields = (
            'notes',
            'zip_file',
            'version',
            'created',
        )

    def get_created(self, obj):
        """Return the release's created info."""
        return self.get_date_time_dict(timestamp=obj.created)


class ProjectReleaseSerializer(ModelSerializer):
    """Base ProjectRelease Serializer for creating and retrieving."""

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
        """Return the project's class."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_class" attribute.'
        )

    @property
    def project_type(self):
        """Return the project's type."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_type" attribute.'
        )

    @property
    def zip_parser(self):
        """Return the project's zip parsing function."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_class" attribute.'
        )

    def get_project_kwargs(self, parent_project=None):
        """Return kwargs for the project."""
        return {
            'pk': self.context['view'].kwargs.get('pk')
        }

    def validate(self, attrs):
        """Validate that the new release can be created."""
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
        attrs['basename'] = basename
        return attrs

    def create(self, validated_data):
        """Update the project's modified datetime when release is created."""
        instance = super().create(validated_data=validated_data)
        getattr(instance, self.project_type.replace('-', '_')).update(
            modified=instance.created,
        )
        return instance


class ProjectImageSerializer(ModelSerializer):
    """Base ProjectImage Serializer."""

    class Meta:
        fields = (
            'image',
        )

    def create(self, validated_data):
        """Add the project to the validated_data when creating the image."""
        view = self.context['view']
        validated_data[view.project_type.replace('-', '_')] = view.project
        return super().create(validated_data=validated_data)
