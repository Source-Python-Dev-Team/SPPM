"""Common models used for inheritance."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from operator import attrgetter
import uuid

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

# 3rd-Party Django
from model_utils.fields import AutoCreatedField
from PIL import Image
from precise_bbcode.fields import BBCodeTextField

# App
from .constants import (
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
from .helpers import (
    handle_project_image_upload,
    handle_project_logo_upload,
    handle_release_zip_file_upload,
)
from .validators import version_validator


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'AbstractUUIDPrimaryKeyModel',
    'ProjectBase',
    'ProjectContributor',
    'ProjectGame',
    'ProjectImage',
    'ProjectRelease',
    'ProjectTag',
)


# =============================================================================
# >> MODELS
# =============================================================================
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
    download_requirements = models.ManyToManyField(
        to='requirements.DownloadRequirement',
        related_name='required_in_%(class)ss',
    )
    logo = models.ImageField(
        upload_to=handle_project_logo_upload,
        blank=True,
        null=True,
        help_text="The project's logo image.",
    )
    owner = models.ForeignKey(
        to='users.ForumUser',
        related_name='%(class)ss',
    )
    package_requirements = models.ManyToManyField(
        to='packages.Package',
        related_name='required_in_%(class)ss',
    )
    pypi_requirements = models.ManyToManyField(
        to='requirements.PyPiRequirement',
        related_name='required_in_%(class)ss',
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
    vcs_requirements = models.ManyToManyField(
        to='requirements.VersionControlRequirement',
        related_name='required_in_%(class)ss',
    )
    created = models.DateTimeField(
        verbose_name='created',
    )
    updated = models.DateTimeField(
        verbose_name='updated',
    )
    basename = None
    logo_path = None

    class Meta:
        abstract = True

    def __str__(self):
        """Return the object's name when str cast."""
        return self.name

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
        errors = dict()
        logo_errors = self.clean_logo()
        if logo_errors:
            errors['logo'] = logo_errors
        if errors:
            raise ValidationError(errors)
        return super().clean()

    def clean_logo(self):
        """Verify the logo is within the proper dimensions."""
        errors = list()
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

    def save(self, *args, **kwargs):
        """Store the slug and remove old logo if necessary."""
        self.slug = self.get_slug_value()
        if all([
            self.logo_path is not None,
            self.logo,
            self.logo_path not in str(self.logo)
        ]):
            path = settings.MEDIA_ROOT / self.logo_path
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.slug]
                if logo:
                    logo[0].remove()
        super().save(*args, **kwargs)

    def get_forum_url(self):
        """Return the forum topic URL."""
        if self.topic is not None:
            return FORUM_THREAD_URL.format(topic=self.topic)
        return None

    def get_slug_value(self):
        """Return the project's slug value."""
        return slugify(self.basename).replace('_', '-')


class ProjectRelease(models.Model):
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
        abstract = True
        verbose_name = 'Release'
        verbose_name_plural = 'Releases'

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


class AbstractUUIDPrimaryKeyModel(models.Model):
    """Abstract model that creates an non-editable UUID primary key."""

    id = models.UUIDField(
        verbose_name='ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class ProjectImage(AbstractUUIDPrimaryKeyModel):
    """Base model for project images."""

    image = models.ImageField(
        upload_to=handle_project_image_upload,
    )
    created = AutoCreatedField(
        verbose_name='created',
    )

    class Meta:
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
    )

    class Meta:
        abstract = True

    def __str__(self):
        """Return the base string."""
        return 'Project Contributor'

    @property
    def project(self):
        """Return the project."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"project" attribute.'
        )

    def clean(self):
        """Validate that the project's owner cannot be a contributor."""
        if self.project.owner == self.user:
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
    )

    class Meta:
        abstract = True

    def __str__(self):
        """Return the base string."""
        return 'Project Game'


class ProjectTag(AbstractUUIDPrimaryKeyModel):
    """Base through model for project tags."""

    tag = models.ForeignKey(
        to='tags.Tag',
    )

    class Meta:
        abstract = True

    def __str__(self):
        """Return the base string."""
        return 'Project Tag'
