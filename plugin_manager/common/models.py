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
from precise_bbcode.fields import BBCodeTextField

# App
from .constants import LOGO_MAX_HEIGHT, LOGO_MAX_WIDTH
from .validators import basename_validator, version_validator
from ..users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'CommonBase',
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
    version = models.CharField(
        max_length=8,
        validators=[version_validator]
    )
    version_notes = BBCodeTextField(
        max_length=512,
        blank=True,
        null=True,
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
    date_created = models.DateTimeField(
        'date created',
        auto_now_add=True,
    )
    date_last_updated = models.DateTimeField(
        'date last updated',
        blank=True,
        null=True,
    )
    description = BBCodeTextField(
        max_length=1024,
        blank=True,
        null=True,
    )
    synopsis = models.CharField(
        max_length=128,
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
                'Logo width must be no more than {0}.'.format(
                    LOGO_MAX_WIDTH)
            )
        if height > LOGO_MAX_HEIGHT:
            errors.append(
                'Logo height must be no more than {0}.'.format(
                    LOGO_MAX_HEIGHT)
            )
        return errors

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        """Store the slug and release data."""
        self.slug = slugify(self.basename).replace('_', '-')

        # TODO: Set the user_id based on the user that is logged in
        if not self.owner_id:
            from random import choice
            self.owner = choice(ForumUser.objects.all())

        super(CommonBase, self).save(
            force_insert, force_update, using, update_fields
        )

    class Meta:
        abstract = True
