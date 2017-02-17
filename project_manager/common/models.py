# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

# 3rd-Party Django
from model_utils.models import TimeStampedModel
from PIL import Image
from precise_bbcode.fields import BBCodeTextField

# App
from .constants import FORUM_THREAD_URL, LOGO_MAX_HEIGHT, LOGO_MAX_WIDTH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'CommonBase',
    'DownloadRequirement',
    'Release',
    'VersionControlRequirement',
)


# =============================================================================
# >> MODELS
# =============================================================================
class CommonBase(models.Model):
    """Base model for upload content."""
    configuration = BBCodeTextField(
        max_length=1024,
        blank=True,
        null=True,
        help_text=(
            'The configuration of the project. If too long, post on the forum '
            'and provide the link here. BBCode is allowed. 1024 char limit.'
        )
    )
    contributors = models.ManyToManyField(
        to='project_manager.ForumUser',
        related_name='%(class)s_contributions',
    )
    description = BBCodeTextField(
        max_length=1024,
        blank=True,
        null=True,
        help_text=(
            'The full description of the project. BBCode is allowed. '
            '1024 char limit.'
        )
    )
    download_requirements = models.ManyToManyField(
        to='project_manager.DownloadRequirement',
        related_name='%(class)ss',
    )
    owner = models.ForeignKey(
        to='project_manager.ForumUser',
        related_name='%(class)ss',
    )
    package_requirements = models.ManyToManyField(
        to='packages.Package',
        related_name='required_in_%(class)ss',
    )
    pypi_requirements = models.ManyToManyField(
        to='project_manager.PyPiRequirement',
        related_name='required_in_%(class)ss',
    )
    supported_games = models.ManyToManyField(
        to='project_manager.Game',
        related_name='%(class)ss',
    )
    synopsis = BBCodeTextField(
        max_length=128,
        blank=True,
        null=True,
        help_text=(
            'A brief description of the project. BBCode is allowed. '
            '128 char limit.'
        )
    )
    tags = models.ManyToManyField(
        to='project_manager.Tag',
        related_name='%(class)ss',
    )
    topic = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
    )
    vcs_requirements = models.ManyToManyField(
        to='project_manager.VersionControlRequirement',
        related_name='%(class)ss',
    )

    class Meta:
        abstract = True

    def __str__(self):
        """Return the object's name when str cast."""
        return self.name

    @property
    def logo(self):
        raise NotImplementedError(
            'Class "{class_name}" must implement "logo" field.'.format(
                class_name=self.__class__.__name__,
            )
        )

    @property
    def releases(self):
        raise NotImplementedError(
            'Class "{class_name}" must implement "releases" field from '
            'ForeignKey.'.format(class_name=self.__class__.__name__)
        )

    @property
    def current_version(self):
        return self.releases.values_list(
            'version',
            flat=True,
        ).order_by(
            '-created'
        )[0]

    @property
    def datetime_created(self):
        return self.releases.values_list(
            'created',
            flat=True
        ).order_by('created')[0]

    @property
    def datetime_last_updated(self):
        release_datetimes = self.releases.values_list(
            'created',
            flat=True,
        ).order_by('-created')
        if len(release_datetimes) == 1:
            return None
        return release_datetimes[0]

    @property
    def total_downloads(self):
        return sum(self.releases.values_list('download_count', flat=True))

    def clean(self):
        """Clean all attributes and raise any errors that occur."""
        errors = dict()
        logo_errors = self.clean_logo()
        if logo_errors:
            errors['logo'] = logo_errors
        if errors:
            raise ValidationError(errors)
        return super(CommonBase, self).clean()

    def clean_logo(self):
        """Verify the logo is within the proper dimensions."""
        errors = list()
        if not self.logo:
            return errors
        width, height = Image.open(self.logo).size
        if width > LOGO_MAX_WIDTH:
            errors.append(
                'Logo width must be no more than {max_width}.'.format(
                    max_width=LOGO_MAX_WIDTH,
                )
            )
        if height > LOGO_MAX_HEIGHT:
            errors.append(
                'Logo height must be no more than {max_height}.'.format(
                    max_height=LOGO_MAX_HEIGHT,
                )
            )
        return errors

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        """Store the slug and release data."""
        self.slug = slugify(self.basename)

        super(CommonBase, self).save(
            force_insert, force_update, using, update_fields
        )

    def get_forum_url(self):
        if self.topic is not None:
            return FORUM_THREAD_URL.format(topic=self.topic)
        return None


class Release(TimeStampedModel):
    download_count = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        abstract = True

    @property
    def file_name(self):
        return self.zip_file.name.rsplit('/', 1)[1]

    @property
    def zip_file(self):
        raise NotImplementedError(
            'Class "{class_name}" must implement "zip_file" field.'.format(
                class_name=self.__class__.__name__,
            )
        )


class VersionControlRequirement(models.Model):
    GIT = 0
    MERCURIAL = 1
    SUBVERSION = 2
    BAZAAR = 3

    SUPPORTED_VCS_TYPES = {
        GIT: 'git',
        MERCURIAL: 'hg',
        SUBVERSION: 'svn',
        BAZAAR: 'bzr',
    }

    name = models.CharField(
        max_length=64,
    )
    vcs_type = models.PositiveSmallIntegerField(
        choices=tuple(SUPPORTED_VCS_TYPES.items()),
        help_text='The type of Version Control used in the url.',
        db_index=True,
        editable=False,
        null=True,
    )
    url = models.CharField(
        max_length=128,
    )

    class Meta:
        verbose_name = 'Version Control Requirement'
        verbose_name_plural = 'Version Control Requirements'


class DownloadRequirement(models.Model):
    name = models.CharField(
        max_length=64,
    )
    url = models.CharField(
        max_length=128,
    )
    description = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Download Requirement'
        verbose_name_plural = 'Download Requirements'
