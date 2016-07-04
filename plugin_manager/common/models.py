# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from __future__ import unicode_literals
from PIL import Image

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

# 3rd-Party Django
from model_utils.models import TimeStampedModel
from precise_bbcode.fields import BBCodeTextField

# App
from .constants import LOGO_MAX_HEIGHT, LOGO_MAX_WIDTH
from .validators import basename_validator, version_validator


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'CommonBase',
    'Release',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
class CommonBase(models.Model):
    """Base model for upload content."""
    name = models.CharField(
        max_length=64,
        unique=True,
    )
    basename = models.CharField(
        max_length=32,
        validators=[basename_validator],
        unique=True,
        blank=True,
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        blank=True,
    )
    synopsis = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    description = BBCodeTextField(
        max_length=1024,
        blank=True,
        null=True,
    )
    configuration = BBCodeTextField(
        max_length=1024,
        blank=True,
        null=True,
    )

    def __str__(self):
        """Return the object's name when str cast."""
        return self.name

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
        self.slug = slugify(self.basename).replace('_', '-')

        super(CommonBase, self).save(
            force_insert, force_update, using, update_fields
        )

    class Meta:
        abstract = True


class Release(TimeStampedModel):
    version = models.CharField(
        max_length=8,
        validators=[version_validator]
    )
    notes = BBCodeTextField(
        max_length=512,
        blank=True,
        null=True,
    )
    download_count = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        abstract = True

    @property
    def file_name(self):
        return self.zip_file.name.rsplit('/', 1)[1]
