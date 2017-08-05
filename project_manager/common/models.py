# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from operator import attrgetter

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
    'Release',
)


# =============================================================================
# >> MODELS
# =============================================================================
class CommonBase(TimeStampedModel):
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
        to='users.ForumUser',
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
        to='requirements.DownloadRequirement',
        related_name='required_in_%(class)ss',
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
    supported_games = models.ManyToManyField(
        to='games.Game',
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
        to='tags.Tag',
        related_name='%(class)ss',
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

    class Meta:
        abstract = True

    def __str__(self):
        """Return the object's name when str cast."""
        return self.name

    @property
    def logo(self):
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement "logo" field.'
        )

    @property
    def releases(self):
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement '
            '"releases" field from ForeignKey.'
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
        return super(CommonBase, self).clean()

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
            f'Class "{self.__class__.__name__}" must implement '
            '"zip_file" field.'
        )
