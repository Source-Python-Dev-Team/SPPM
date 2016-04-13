# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import unicode_literals
from collections import defaultdict
from PIL import Image

# 3rd-Party Python
from path import Path

# Django Imports
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

# 3rd-Party Django Imports
from precise_bbcode.fields import BBCodeTextField

# Project Imports
from users.models import User

# App Imports
from .constants import LOGO_MAX_HEIGHT, LOGO_MAX_WIDTH
from .validators import basename_validator, version_validator


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
    name = models.CharField(
        max_length=64,
        unique=True,
        null=False,
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
    current_version = models.CharField(
        max_length=8,
        blank=True,
        null=True,
    )
    current_version_notes = BBCodeTextField(
        max_length=512,
        blank=True,
        null=True,
    )
    current_zip_file = models.FileField(
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

    logo = None

    def __str__(self):
        return self.name

    @property
    def old_release_class(self):
        raise NotImplementedError('No old release class set for class.')

    def clean(self):
        errors = defaultdict(list)
        self.clean_logo(errors)
        if errors:
            raise ValidationError(errors)
        return super(CommonBase, self).clean()

    def clean_logo(self, errors):
        if not self.logo:
            return
        width, height = Image.open(self.logo).size
        if width > LOGO_MAX_WIDTH:
            errors['logo'].append(
                'Logo width must be no more than {0}.'.format(
                    LOGO_MAX_WIDTH)
            )
        if height > LOGO_MAX_HEIGHT:
            errors['logo'].append(
                'Logo height must be no more than {0}.'.format(
                    LOGO_MAX_HEIGHT)
            )

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        self.slug = slugify(self.basename).replace('_', '-')

        # TODO: Set the user_id based on the user that is logged in
        from random import choice
        if not self.user_id:
            self.user_id = choice(User.objects.all()).pk

        if self.current_version and self.current_zip_file:
            release = self.old_release_class(
                version=self.current_version,
                version_notes=self.current_version_notes,
                zip_file=self.current_zip_file,
                plugin=self,
            )
            release.save()
            self.previous_releases.add(release)

        self.current_version = self.version
        self.current_version_notes = self.version_notes
        self.current_zip_file = self.zip_file

        if self.logo and u'logo/' not in self.logo:
            path = Path(settings.MEDIA_ROOT) / 'logos' / 'plugins'
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.basename]
                if logo:
                    logo[0].remove()

        super(CommonBase, self).save(
            force_insert, force_update, using, update_fields
        )

    class Meta:
        abstract = True
