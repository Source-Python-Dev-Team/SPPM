"""Common serializers for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from datetime import datetime
from typing import Any

# Django
from django.utils.timezone import now

# Third Party Django
from embed_video.backends import detect_backend
from rest_framework.exceptions import ValidationError
from rest_framework.fields import (
    CharField,
    FileField,
    IntegerField,
    SerializerMethodField,
    URLField,
)
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

# App
from games.api.common.serializers import MinimalGameSerializer
from games.constants import GAME_SLUG_MAX_LENGTH
from games.models import Game
from project_manager.api.common.serializers.mixins import (
    CreateRequirementsMixin,
    ProjectLocaleMixin,
    ProjectReleaseCreationMixin,
    ProjectThroughMixin,
)
from project_manager.constants import (
    IMAGE_MAX_HEIGHT,
    IMAGE_MAX_WIDTH,
    RELEASE_NOTES_MAX_LENGTH,
    RELEASE_VERSION_MAX_LENGTH,
)
from project_manager.models.abstract import Project, ProjectRelease
from tags.constants import TAG_NAME_MAX_LENGTH
from tags.models import Tag
from users.api.common.serializers import ForumUserContributorSerializer
from users.constants import USER_USERNAME_MAX_LENGTH
from users.models import ForumUser

# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    "ProjectContributorSerializer",
    "ProjectCreateReleaseSerializer",
    "ProjectGameSerializer",
    "ProjectImageSerializer",
    "ProjectReleaseSerializer",
    "ProjectSerializer",
    "ProjectTagSerializer",
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
project_release_meta = vars(ProjectRelease)["_meta"]


# =============================================================================
# SERIALIZERS
# =============================================================================
class ProjectSerializer(
    CreateRequirementsMixin,
    ModelSerializer,
    ProjectLocaleMixin,
):
    """Base Project Serializer."""

    current_release = SerializerMethodField()
    owner = ForumUserContributorSerializer(
        read_only=True,
    )
    contributors = SerializerMethodField()
    created = SerializerMethodField()
    updated = SerializerMethodField()
    video = URLField(
        required=False,
        write_only=True,
    )
    video_embed_html = SerializerMethodField(
        read_only=True,
    )

    release_dict = {}

    class Meta:
        """Define metaclass attributes."""

        fields = (
            "name",
            "slug",
            "total_downloads",
            "current_release",
            "created",
            "updated",
            "synopsis",
            "description",
            "configuration",
            "logo",
            "video",
            "video_embed_html",
            "owner",
            "contributors",
        )
        read_only_fields = (
            "slug",
        )

    @property
    def project_type(self) -> str:
        """Return the project's type."""
        msg = (
            f'Class "{self.__class__.__name__}" must implement a '
            '"project_type" attribute.'
        )
        raise NotImplementedError(msg)

    @property
    def release_model(self) -> type[ProjectRelease]:
        """Return the model to use for releases."""
        msg = (
            f'Class "{self.__class__.__name__}" must implement a '
            '"release_model" attribute.'
        )
        raise NotImplementedError(msg)

    def get_fields(self) -> dict:
        """Only include contributors in the list view."""
        fields = super().get_fields()
        view = self.context.get("view")
        if view and view.action != "list":
            fields.pop("contributors", None)
        return fields

    def create(self, validated_data: dict) -> Project:
        """Create the instance and the first release of the project."""
        validated_data = self.get_extra_validated_data(validated_data)
        current_time = now()
        validated_data["created"] = validated_data["updated"] = current_time
        instance = super().create(validated_data)
        self.requirements = self.release_dict.pop("requirements")
        kwargs = {
            self.project_type.replace("-", "_"): instance,
            "created": current_time,
            "notes": self.release_dict["notes"],
            "version": self.release_dict["version"],
            "zip_file": self.release_dict["zip_file"],
            "created_by": self.context["request"].user.forum_user,
        }
        release = self.release_model.objects.create(**kwargs)
        self._create_requirements(release=release)
        return instance

    def get_created(self, obj: Project) -> dict[str, datetime]:
        """Return the project's created info."""
        return self.get_date_time_dict(timestamp=obj.created)

    def get_current_release(self, obj: Project) -> dict:
        """Return the current release info."""
        release = obj.releases.first()
        zip_url = reverse(
            viewname=f"{self.project_type}-download",
            kwargs=self.get_download_kwargs(
                obj=obj,
                release=release,
            ),
            request=self.context["request"],
        )
        release_dict = {
            "version": release.version,
            "notes": str(release.notes) if release.notes else release.notes,
            "zip_file": zip_url,
        }
        if self.context["view"].action == "retrieve":
            release_dict.update(self.get_requirements(release))
        return release_dict

    @staticmethod
    def get_requirements(release: ProjectRelease) -> dict[str, list[dict]]:
        """Return a dictionary of requirements for the given release."""
        project_type = release.__class__.__name__.lower()
        package_requirements = [
            {
                "name": item["package_requirement__name"],
                "version": item["version"],
                "optional": item["optional"],
            } for item in
            getattr(release, f"{project_type}packagerequirement_set").values(
                "package_requirement__name",
                "version",
                "optional",
            )
        ]
        pypi_requirements = [
            {
                "name": item["pypi_requirement__name"],
                "version": item["version"],
                "optional": item["optional"],
            } for item in
            getattr(release, f"{project_type}pypirequirement_set").values(
                "pypi_requirement__name",
                "version",
                "optional",
            )
        ]
        vcs_requirements = [
            {
                "url": item["vcs_requirement__url"],
                "version": item["version"],
                "optional": item["optional"],
            } for item in
            getattr(
                release,
                f"{project_type}versioncontrolrequirement_set",
            ).values(
                "vcs_requirement__url",
                "version",
                "optional",
            )
        ]
        download_requirements = [
            {
                "url": item["download_requirement__url"],
                "optional": item["optional"],
            } for item in
            getattr(release, f"{project_type}downloadrequirement_set").values(
                "download_requirement__url",
                "optional",
            )
        ]
        return {
            "package_requirements": package_requirements,
            "pypi_requirements": pypi_requirements,
            "version_control_requirements": vcs_requirements,
            "download_requirements": download_requirements,
        }

    def get_extra_validated_data(self, validated_data: dict) -> dict:
        """Add any extra data to be used on create."""
        validated_data["owner"] = self.context["request"].user.forum_user
        validated_data["basename"] = self.release_dict["basename"]
        return validated_data

    @staticmethod
    def get_contributors(obj: Project) -> str:
        """Return a comma-separated list of contributors."""
        return ", ".join(
            contributor.user.username
            for contributor in obj.contributors.all()
        )

    def get_updated(self, obj: Project) -> dict[str, datetime]:
        """Return the project's last updated info."""
        return self.get_date_time_dict(timestamp=obj.updated)

    @staticmethod
    def get_video_embed_html(obj: Project) -> type[str | None]:
        """Return the video embed url."""
        if not obj.video:
            return None

        backend = detect_backend(str(obj.video))
        code = backend.get_embed_code(
            width=IMAGE_MAX_WIDTH,
            height=IMAGE_MAX_HEIGHT,
        )
        return code.replace(
            "></iframe>",
            ' referrerpolicy="strict-origin-when-cross-origin"></iframe>',
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate the given field values."""
        self.release_dict = attrs.pop("initial_release", {})
        return attrs

    def update(self, instance: Project, validated_data: dict) -> Project:
        """Do not allow the project's 'name' to be updated via API."""
        with suppress(KeyError):
            del validated_data["name"]
        return super().update(instance=instance, validated_data=validated_data)

    @staticmethod
    def get_download_kwargs(obj: Project, release: ProjectRelease) -> dict:
        """Return the release's reverse kwargs."""
        return {
            "slug": obj.slug,
            "zip_file": release.file_name,
        }


class ProjectReleaseSerializer(
    ProjectReleaseCreationMixin, ProjectLocaleMixin,
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
            "notes",
            "zip_file",
            "version",
            "created",
            "created_by",
            "download_count",
            "download_requirements",
            "package_requirements",
            "pypi_requirements",
            "vcs_requirements",
        )

    def get_created(self, obj: ProjectRelease) -> dict[str, datetime]:
        """Return the release's created info."""
        return self.get_date_time_dict(timestamp=obj.created)


class ProjectCreateReleaseSerializer(ProjectReleaseCreationMixin):
    """Base ProjectRelease Serializer for creating and retrieving."""

    notes = CharField(
        max_length=RELEASE_NOTES_MAX_LENGTH,
        allow_blank=True,
        help_text=project_release_meta.get_field("notes").help_text,
    )
    version = CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        allow_blank=True,
        help_text=project_release_meta.get_field("version").help_text,
    )
    zip_file = FileField(
        allow_null=True,
        help_text=project_release_meta.get_field("zip_file").help_text,
    )

    class Meta:
        """Define metaclass attributes."""

        model = None
        fields = (
            "notes",
            "zip_file",
            "version",
        )


class ProjectImageSerializer(ProjectThroughMixin):
    """Base ProjectImage Serializer."""

    class Meta:
        """Define metaclass attributes."""

        fields = (
            "image",
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
            "game_slug",
            "game",
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate the given game."""
        name = attrs.pop("game_slug")
        view = self.context["view"]
        if view.project.supported_games.filter(slug=name).exists():
            raise ValidationError({
                "game": f"Game already linked to {view.project_type}.",
            })

        try:
            game = Game.objects.get(basename=name)
        except Game.DoesNotExist as exception:
            raise ValidationError({
                "game": f'Invalid game "{name}".',
            }) from exception

        attrs["game"] = game
        return super().validate(attrs=attrs)


class ProjectTagSerializer(ProjectThroughMixin):
    """Base ProjectTag Serializer."""

    tag = CharField(
        max_length=TAG_NAME_MAX_LENGTH,
    )

    class Meta:
        """Define metaclass attributes."""

        fields = (
            "tag",
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate the given tag."""
        name = attrs["tag"]
        view = self.context["view"]
        if view.project.tags.filter(name=name).exists():
            raise ValidationError({
                "tag": f"Tag already linked to {view.project_type}.",
            })

        tag, _ = Tag.objects.get_or_create(
            name=name,
            defaults={
                "creator": view.request.user.forum_user,
            },
        )
        if tag.black_listed:
            raise ValidationError({
                "tag": f"Tag '{name}' is black-listed, unable to add.",
            })

        attrs["tag"] = tag
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
            "username",
            "user",
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate the given username."""
        username = attrs.pop("username")
        view = self.context["view"]
        if view.project.contributors.filter(user__username=username).exists():
            raise ValidationError({
                "username": f"User {username} is already a contributor",
            })

        if username == view.project.owner.user.username:
            raise ValidationError({
                "username": (
                    f"User {username} is the owner, "
                    f"cannot add as a contributor"
                ),
            })

        try:
            user = ForumUser.objects.get(user__username=username)
        except ForumUser.DoesNotExist as exception:
            raise ValidationError({
                "username": f'No user named "{username}".',
            }) from exception

        attrs["user"] = user
        return super().validate(attrs=attrs)
