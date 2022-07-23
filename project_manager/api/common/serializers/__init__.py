"""Common serializers for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
from contextlib import suppress

# Django
from django.utils.timezone import now

# Third Party Django
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
from project_manager.api.common.serializers.mixins import (
    CreateRequirementsMixin,
    ProjectLocaleMixin,
    ProjectReleaseCreationMixin,
    ProjectThroughMixin,
)
from project_manager.constants import (
    RELEASE_NOTES_MAX_LENGTH,
    RELEASE_VERSION_MAX_LENGTH,
)
from games.api.common.serializers import MinimalGameSerializer
from games.constants import GAME_SLUG_MAX_LENGTH
from games.models import Game
from tags.constants import TAG_NAME_MAX_LENGTH
from tags.models import Tag
from users.api.common.serializers import ForumUserContributorSerializer
from users.constants import USER_USERNAME_MAX_LENGTH
from users.models import ForumUser


# =============================================================================
# ALL DECLARATION
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
# SERIALIZERS
# =============================================================================
class ProjectSerializer(
    CreateRequirementsMixin,
    ModelSerializer,
    ProjectLocaleMixin
):
    """Base Project Serializer."""

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

    release_dict = {}

    class Meta:
        """Define metaclass attributes."""

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
            'contributors',
        )
        read_only_fields = (
            'slug',
        )

    @property
    def project_type(self):
        """Return the project's type."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"project_type" attribute.'
        )

    @property
    def release_model(self):
        """Return the model to use for releases."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"release_model" attribute.'
        )

    def get_fields(self):
        """Only include contributors in the list view."""
        fields = super().get_fields()
        if self.context['view'].action != 'list':
            del fields['contributors']
        return fields

    def create(self, validated_data):
        """Create the instance and the first release of the project."""
        validated_data = self.get_extra_validated_data(validated_data)
        current_time = now()
        validated_data['created'] = validated_data['updated'] = current_time
        instance = super().create(validated_data)
        self.requirements = self.release_dict.pop('requirements')
        kwargs = {
            self.project_type.replace('-', '_'): instance,
            'created': current_time,
            'notes': self.release_dict['notes'],
            'version': self.release_dict['version'],
            'zip_file': self.release_dict['zip_file'],
            'created_by': self.context['request'].user.forum_user,
        }
        release = self.release_model.objects.create(**kwargs)
        self._create_requirements(release=release)
        return instance

    def get_created(self, obj):
        """Return the project's created info."""
        return self.get_date_time_dict(timestamp=obj.created)

    def get_current_release(self, obj):
        """Return the current release info."""
        release = obj.releases.first()
        zip_url = reverse(
            viewname=f'{self.project_type}-download',
            kwargs=self.get_download_kwargs(
                obj=obj,
                release=release,
            ),
            request=self.context['request']
        )
        release_dict = {
            'version': release.version,
            'notes': str(release.notes) if release.notes else release.notes,
            'zip_file': zip_url,
        }
        if self.context['view'].action == 'retrieve':
            release_dict.update(self.get_requirements(release))
        return release_dict

    @staticmethod
    def get_requirements(release):
        """Return a dictionary of requirements for the given release."""
        project_type = release.__class__.__name__.lower()
        package_requirements = [
            {
                'name': item['package_requirement__name'],
                'version': item['version'],
                'optional': item['optional'],
            } for item in
            getattr(release, f'{project_type}packagerequirement_set').values(
                'package_requirement__name',
                'version',
                'optional',
            )
        ]
        pypi_requirements = [
            {
                'name': item['pypi_requirement__name'],
                'version': item['version'],
                'optional': item['optional'],
            } for item in
            getattr(release, f'{project_type}pypirequirement_set').values(
                'pypi_requirement__name',
                'version',
                'optional',
            )
        ]
        vcs_requirements = [
            {
                'url': item['vcs_requirement__url'],
                'version': item['version'],
                'optional': item['optional'],
            } for item in
            getattr(
                release,
                f'{project_type}versioncontrolrequirement_set'
            ).values(
                'vcs_requirement__url',
                'version',
                'optional',
            )
        ]
        download_requirements = [
            {
                'url': item['download_requirement__url'],
                'optional': item['optional'],
            } for item in
            getattr(release, f'{project_type}downloadrequirement_set').values(
                'download_requirement__url',
                'optional',
            )
        ]
        return {
            'package_requirements': package_requirements,
            'pypi_requirements': pypi_requirements,
            'version_control_requirements': vcs_requirements,
            'download_requirements': download_requirements,
        }

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
    created_by = ForumUserContributorSerializer(
        read_only=True,
    )
    download_count = IntegerField(read_only=True)

    class Meta:
        """Define metaclass attributes."""

        model = None
        fields = (
            'notes',
            'zip_file',
            'version',
            'created',
            'created_by',
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
        """Define metaclass attributes."""

        model = None
        fields = (
            'notes',
            'zip_file',
            'version',
        )


class ProjectImageSerializer(ProjectThroughMixin):
    """Base ProjectImage Serializer."""

    class Meta:
        """Define metaclass attributes."""

        fields = (
            'image',
        )


class ProjectGameSerializer(ProjectThroughMixin):
    """Base ProjectGame Serializer."""

    game_slug = CharField(
        max_length=GAME_SLUG_MAX_LENGTH,
        write_only=True,
    )
    game = MinimalGameSerializer(
        read_only=True,
    )

    class Meta:
        """Define metaclass attributes."""

        fields = (
            'game_slug',
            'game',
        )

    def validate(self, attrs):
        """Validate the given game."""
        name = attrs.pop('game_slug')
        view = self.context['view']
        if view.project.supported_games.filter(slug=name).exists():
            raise ValidationError({
                'game': f'Game already linked to {view.project_type}.',
            })

        try:
            game = Game.objects.get(basename=name)
        except Game.DoesNotExist as exception:
            raise ValidationError({
                'game': f'Invalid game "{name}".'
            }) from exception

        attrs['game'] = game
        return super().validate(attrs=attrs)


class ProjectTagSerializer(ProjectThroughMixin):
    """Base ProjectTag Serializer."""

    tag = CharField(
        max_length=TAG_NAME_MAX_LENGTH,
    )

    class Meta:
        """Define metaclass attributes."""

        fields = (
            'tag',
        )

    def validate(self, attrs):
        """Validate the given tag."""
        name = attrs['tag']
        view = self.context['view']
        if view.project.tags.filter(name=name).exists():
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
        """Define metaclass attributes."""

        fields = (
            'username',
            'user',
        )

    def validate(self, attrs):
        """Validate the given username."""
        username = attrs.pop('username')
        view = self.context['view']
        if view.project.contributors.filter(user__username=username).exists():
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
        except ForumUser.DoesNotExist as exception:
            raise ValidationError({
                'username': f'No user named "{username}".'
            }) from exception

        attrs['user'] = user
        return super().validate(attrs=attrs)
