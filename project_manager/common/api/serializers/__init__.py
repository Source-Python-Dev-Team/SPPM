"""Common serializers for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress

# Django
from django.utils.timezone import now

# 3rd-Party Django
from rest_framework.exceptions import ValidationError
from rest_framework.fields import (
    CharField,
    FileField,
    IntegerField,
    SerializerMethodField,
)
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

# App
from project_manager.common.api.serializers.mixins import (
    ProjectLocaleMixin,
    ProjectReleaseCreationMixin,
    ProjectThroughMixin,
)
from project_manager.common.constants import (
    RELEASE_NOTES_MAX_LENGTH,
    RELEASE_VERSION_MAX_LENGTH,
)
from project_manager.constants import USER_USERNAME_MAX_LENGTH
from project_manager.games.api.serializers import GameSerializer
from project_manager.games.constants import GAME_SLUG_MAX_LENGTH
from project_manager.games.models import Game
from project_manager.tags.constants import TAG_NAME_MAX_LENGTH
from project_manager.tags.models import Tag
from project_manager.users.api.serializers.common import (
    ForumUserContributorSerializer,
)
from project_manager.users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectContributorSerializer',
    'ProjectCreateReleaseSerializer',
    'ProjectGameSerializer',
    'ProjectImageSerializer',
    'ProjectReleaseSerializer',
    'ProjectSerializer',
    'ProjectTagSerializer',
)


# =============================================================================
# >> SERIALIZERS
# =============================================================================
class ProjectSerializer(ModelSerializer, ProjectLocaleMixin):
    """Base Project Serializer."""

    current_release = SerializerMethodField()
    owner = ForumUserContributorSerializer(
        read_only=True,
    )
    created = SerializerMethodField()
    updated = SerializerMethodField()

    release_dict = {}

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
            'video',
            'owner',
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
        validated_data = self.get_extra_validated_data(validated_data)
        current_time = now()
        validated_data['created'] = validated_data['updated'] = current_time
        instance = super().create(validated_data)
        version = self.release_dict['version']
        zip_file = self.release_dict['zip_file']
        notes = self.release_dict['notes']
        kwargs = {
            '{project_type}'.format(
                project_type=self.project_type.replace('-', '_')
            ): instance,
            'created': current_time,
            'notes': notes,
            'version': version,
            'zip_file': zip_file,
        }
        self.release_model.objects.create(**kwargs)
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

    def get_extra_validated_data(self, validated_data):
        """Add any extra data to be used on create."""
        validated_data['owner'] = self.context['request'].user.forum_user
        validated_data['basename'] = self.release_dict['basename']
        return validated_data

    def get_updated(self, obj):
        """Return the project's last updated info."""
        return self.get_date_time_dict(timestamp=obj.updated)

    def validate(self, attrs):
        """Validate the given field values."""
        self.release_dict = attrs.pop('releases', {})
        version = self.release_dict.get('version', '')
        zip_file = self.release_dict.get('zip_file')
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

    def update(self, instance, validated_data):
        """Do not allow the project's 'name' to be updated via API."""
        with suppress(KeyError):
            del validated_data['name']
        return super().update(instance=instance, validated_data=validated_data)

    @staticmethod
    def get_download_kwargs(obj, release):
        """Return the release's reverse kwargs."""
        return {
            'slug': obj.slug,
            'zip_file': release.file_name,
        }


class ProjectReleaseSerializer(
    ProjectReleaseCreationMixin, ProjectLocaleMixin
):
    """Base ProjectRelease Serializer for listing."""

    created = SerializerMethodField()
    download_count = IntegerField(read_only=True)

    class Meta:
        model = None
        fields = (
            'notes',
            'zip_file',
            'version',
            'created',
            'download_count',
            'download_requirements',
            'package_requirements',
            'pypi_requirements',
            'vcs_requirements',
        )

    def get_created(self, obj):
        """Return the release's created info."""
        return self.get_date_time_dict(timestamp=obj.created)


class ProjectCreateReleaseSerializer(ProjectReleaseCreationMixin):
    """Base ProjectRelease Serializer for creating and retrieving."""

    notes = CharField(
        max_length=RELEASE_NOTES_MAX_LENGTH,
        allow_blank=True,
    )
    version = CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        allow_blank=True,
    )
    zip_file = FileField(
        allow_null=True,
    )

    class Meta:
        model = None
        fields = (
            'notes',
            'zip_file',
            'version',
        )


class ProjectImageSerializer(ProjectThroughMixin):
    """Base ProjectImage Serializer."""

    add_project = False

    class Meta:
        fields = (
            'image',
        )

    def create(self, validated_data):
        """Add the project to the validated_data when creating the image."""
        view = self.context['view']
        validated_data[view.project_type.replace('-', '_')] = view.project
        return super().create(validated_data=validated_data)


class ProjectGameSerializer(ProjectThroughMixin):
    """Base ProjectGame Serializer."""

    game_slug = CharField(
        max_length=GAME_SLUG_MAX_LENGTH,
        write_only=True,
    )
    game = GameSerializer(
        read_only=True,
    )

    class Meta:
        fields = (
            'game_slug',
            'game',
        )

    def validate(self, attrs):
        """Validate the given game."""
        name = attrs.pop('game_slug')
        view = self.context['view']
        if name in view.project.supported_games.values_list('slug', flat=True):
            raise ValidationError({
                'game': f'Game already linked to {view.project_type}.',
            })
        try:
            game = Game.objects.get(basename=name)
        except Game.DoesNotExist:
            raise ValidationError({
                'game': f'Invalid game "{name}".'
            })
        attrs['game'] = game
        return super().validate(attrs=attrs)


class ProjectTagSerializer(ProjectThroughMixin):
    """Base ProjectTag Serializer."""

    tag = CharField(
        max_length=TAG_NAME_MAX_LENGTH,
    )

    class Meta:
        fields = (
            'tag',
        )

    def validate(self, attrs):
        """Validate the given tag."""
        name = attrs['tag']
        view = self.context['view']
        if name in view.project.tags.values_list('name', flat=True):
            raise ValidationError({
                'tag': f'Tag already linked to {view.project_type}.',
            })
        tag, created = Tag.objects.get_or_create(
            name=name,
            defaults={
                'creator': view.request.user.forum_user,
            }
        )
        if tag.black_listed:
            raise ValidationError({
                'tag': f"Tag '{name}' is black-listed, unable to add.",
            })
        attrs['tag'] = tag
        return super().validate(attrs=attrs)


class ProjectContributorSerializer(ProjectThroughMixin):
    """Base ProjectContributor Serializer."""

    username = CharField(
        max_length=USER_USERNAME_MAX_LENGTH,
        write_only=True,
    )
    user = ForumUserContributorSerializer(
        read_only=True,
    )

    class Meta:
        fields = (
            'username',
            'user',
        )

    def validate(self, attrs):
        """Validate the given username."""
        username = attrs.pop('username')
        view = self.context['view']
        if username in view.project.contributors.values_list(
            'user__username',
            flat=True,
        ):
            raise ValidationError({
                'username': f'User {username} is already a contributor',
            })
        if username == view.project.owner.user.username:
            raise ValidationError({
                'username': (
                    f'User {username} is the owner, '
                    f'cannot add as a contributor'
                ),
            })
        try:
            user = ForumUser.objects.get(user__username=username)
        except ForumUser.DoesNotExist:
            raise ValidationError({
                'user': f'No user named "{username}".'
            })
        attrs['user'] = user
        return super().validate(attrs=attrs)
