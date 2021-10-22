"""Common models used for inheritance."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
import uuid
from operator import attrgetter

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

# Third Party Django
from embed_video.fields import EmbedVideoField
from model_utils.fields import AutoCreatedField
from PIL import Image
from precise_bbcode.fields import BBCodeTextField

# App
from project_manager.common.constants import (
    FORUM_THREAD_URL,
    LOGO_MAX_HEIGHT,
    LOGO_MAX_WIDTH,
    PROJECT_CONFIGURATION_MAX_LENGTH,
    PROJECT_DESCRIPTION_MAX_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_SYNOPSIS_MAX_LENGTH,
    RELEASE_NOTES_MAX_LENGTH,
    RELEASE_VERSION_MAX_LENGTH,
)
from project_manager.common.helpers import (
    handle_project_image_upload,
    handle_project_logo_upload,
    handle_release_zip_file_upload,
)
from project_manager.common.validators import version_validator


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'AbstractUUIDPrimaryKeyModel',
    'ProjectBase',
    'ProjectContributor',
    'ProjectGame',
    'ProjectImage',
    'ProjectRelease',
    'ProjectReleaseDownloadRequirement',
    'ProjectReleasePackageRequirement',
    'ProjectReleasePyPiRequirement',
    'ProjectReleaseVersionControlRequirement',
    'ProjectTag',
)


# =============================================================================
# MODELS
# =============================================================================
class AbstractUUIDPrimaryKeyModel(models.Model):
    """Abstract model that creates an non-editable UUID primary key."""

    id = models.UUIDField(
        verbose_name='ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True


class ProjectBase(models.Model):
    """Base model for projects."""

    name = models.CharField(
        max_length=PROJECT_NAME_MAX_LENGTH,
        help_text=(
            "The name of the project. Do not include the version, as that is "
            "added dynamically to the project's page."
        ),
    )
    configuration = BBCodeTextField(
        max_length=PROJECT_CONFIGURATION_MAX_LENGTH,
        blank=True,
        null=True,
        help_text=(
            'The configuration of the project. If too long, post on the forum '
            'and provide the link here. BBCode is allowed. 1024 char limit.'
        )
    )
    description = BBCodeTextField(
        max_length=PROJECT_DESCRIPTION_MAX_LENGTH,
        blank=True,
        null=True,
        help_text=(
            'The full description of the project. BBCode is allowed. '
            '1024 char limit.'
        )
    )
    logo = models.ImageField(
        upload_to=handle_project_logo_upload,
        blank=True,
        null=True,
        help_text="The project's logo image.",
    )
    video = EmbedVideoField(
        null=True,
        help_text="The project's video."
    )
    owner = models.ForeignKey(
        to='users.ForumUser',
        related_name='%(class)ss',
        on_delete=models.CASCADE,
    )
    synopsis = BBCodeTextField(
        max_length=PROJECT_SYNOPSIS_MAX_LENGTH,
        blank=True,
        null=True,
        help_text=(
            'A brief description of the project. BBCode is allowed. '
            '128 char limit.'
        )
    )
    topic = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(
        verbose_name='created',
    )
    updated = models.DateTimeField(
        verbose_name='updated',
    )
    basename = None
    logo_path = None
    slug = None

    class Meta:
        """Define metaclass attributes."""

        abstract = True

    def __str__(self):
        """Return the object's name when str cast."""
        return str(self.name)

    @property
    def handle_logo_upload(self):
        """Return the function to use for handling logo uploads."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"handle_logo_upload" attribute.'
        )

    @property
    def releases(self):
        """Raise error if class doesn't have a related field for 'releases'."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"releases" field via ForeignKey relationship.'
        )

    @property
    def current_version(self):
        """Return the current release's version."""
        return self.releases.values_list(
            'version',
            flat=True,
        ).order_by(
            '-created'
        )[0]

    @property
    def total_downloads(self):
        """Return the total number of downloads for the project."""
        return sum(
            map(
                attrgetter('download_count'),
                self.releases.all()
            )
        )

    def clean(self):
        """Clean all attributes and raise any errors that occur."""
        errors = {}
        logo_errors = self.clean_logo()
        if logo_errors:
            errors['logo'] = logo_errors
        if errors:
            raise ValidationError(errors)
        return super().clean()

    def clean_logo(self):
        """Verify the logo is within the proper dimensions."""
        errors = []
        if not self.logo:
            return errors
        width, height = Image.open(self.logo).size
        if width > LOGO_MAX_WIDTH:
            errors.append(f'Logo width must be no more than {LOGO_MAX_WIDTH}.')
        if height > LOGO_MAX_HEIGHT:
            errors.append(
                f'Logo height must be no more than {LOGO_MAX_HEIGHT}.'
            )
        return errors

    def save(
        self, force_insert=False, force_update=False, using=None,
        update_fields=None
    ):
        """Store the slug and remove old logo if necessary."""
        self.slug = self.get_slug_value()
        if all([
            self.logo_path is not None,
            self.logo,
            self.logo_path not in str(self.logo)
        ]):
            path = settings.MEDIA_ROOT / self.logo_path
            if path.isdir():
                logo = [x for x in path.files() if x.stem == self.slug]
                if logo:
                    logo[0].remove()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def get_forum_url(self):
        """Return the forum topic URL."""
        if self.topic is not None:
            return FORUM_THREAD_URL.format(topic=self.topic)
        return None

    def get_slug_value(self):
        """Return the project's slug value."""
        return slugify(self.basename).replace('_', '-')


class ProjectRelease(AbstractUUIDPrimaryKeyModel):
    """Base model for project releases."""

    version = models.CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        validators=[version_validator],
        help_text='The version for this release of the project.',
    )
    notes = BBCodeTextField(
        max_length=RELEASE_NOTES_MAX_LENGTH,
        blank=True,
        null=True,
        help_text='The notes for this particular release of the project.',
    )
    zip_file = models.FileField(
        upload_to=handle_release_zip_file_upload,
    )
    download_count = models.PositiveIntegerField(
        default=0,
    )
    created = AutoCreatedField(
        verbose_name='created',
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True
        verbose_name = 'Release'
        verbose_name_plural = 'Releases'

    @property
    def project_class(self):
        """Return the project's class."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project_class" attribute.'
        )

    @property
    def project(self):
        """Return the project's class."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project" property.'
        )

    @property
    def file_name(self):
        """Return the name of the zip file."""
        return self.zip_file.name.rsplit('/', 1)[1]

    @property
    def handle_zip_file_upload(self):
        """Return the function to use for handling zip file uploads."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"handle_zip_file_upload" attribute.'
        )

    def __str__(self):
        """Return the project name + release version."""
        return f'{self.project} - {self.version}'

    def save(
        self, force_insert=False, force_update=False, using=None,
        update_fields=None
    ):
        """Update the Project's 'updated' value to the releases 'created'."""
        pk = self.pk
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
        if pk is None:
            self.project_class.objects.filter(
                pk=self.project.pk,
            ).update(
                updated=self.created,
            )


class ProjectImage(AbstractUUIDPrimaryKeyModel):
    """Base model for project images."""

    image = models.ImageField(
        upload_to=handle_project_image_upload,
    )
    created = AutoCreatedField(
        verbose_name='created',
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    @property
    def handle_image_upload(self):
        """Return the function to use for handling image uploads."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"handle_image_upload" attribute.'
        )


class ProjectContributor(AbstractUUIDPrimaryKeyModel):
    """Base through model for project contributors."""

    user = models.ForeignKey(
        to='users.ForumUser',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True

    def __str__(self):
        """Return the base string."""
        return 'Project Contributor'

    @property
    def project(self):
        """Return the project's class."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            f'"project" property.'
        )

    def clean(self):
        """Validate that the project's owner cannot be a contributor."""
        if hasattr(self, 'user') and self.project.owner == self.user:
            raise ValidationError({
                'user': (
                    f'{self.user} is the owner and cannot be added '
                    f'as a contributor.'
                )
            })
        return super().clean()


class ProjectGame(AbstractUUIDPrimaryKeyModel):
    """Base through model for project supported_games."""

    game = models.ForeignKey(
        to='games.Game',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True

    def __str__(self):
        """Return the base string."""
        return 'Project Game'


class ProjectTag(AbstractUUIDPrimaryKeyModel):
    """Base through model for project tags."""

    tag = models.ForeignKey(
        to='tags.Tag',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True

    def __str__(self):
        """Return the base string."""
        return 'Project Tag'


class ProjectReleasePackageRequirement(AbstractUUIDPrimaryKeyModel):
    """Base Package requirement model."""

    package_requirement = models.ForeignKey(
        to='project_manager.Package',
        on_delete=models.CASCADE,
    )
    version = models.CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        validators=[version_validator],
        help_text=(
            'The version of the custom package for this release '
            'of the project.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.package_requirement.name} - {self.version}'


class ProjectReleasePyPiRequirement(AbstractUUIDPrimaryKeyModel):
    """Base PyPi requirement model."""

    pypi_requirement = models.ForeignKey(
        to='requirements.PyPiRequirement',
        on_delete=models.CASCADE,
    )
    version = models.CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        validators=[version_validator],
        help_text=(
            'The version of the PyPi package for this release of the project.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.pypi_requirement.name} - {self.version}'


class ProjectReleaseVersionControlRequirement(AbstractUUIDPrimaryKeyModel):
    """Base VCS requirement model."""

    vcs_requirement = models.ForeignKey(
        to='requirements.VersionControlRequirement',
        on_delete=models.CASCADE,
    )
    version = models.CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        validators=[version_validator],
        help_text=(
            'The version of the VCS package for this release of the project.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.vcs_requirement.url} - {self.version}'


class ProjectReleaseDownloadRequirement(AbstractUUIDPrimaryKeyModel):
    """Base Download requirement model."""

    download_requirement = models.ForeignKey(
        to='requirements.DownloadRequirement',
        on_delete=models.CASCADE,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True

    def __str__(self):
        """Return the requirement's url."""
        return self.download_requirement.url
