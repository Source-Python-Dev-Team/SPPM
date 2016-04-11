# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import unicode_literals

# Django Imports
from django.db import models
from django.utils.text import slugify

# 3rd-Party Django Imports
from precise_bbcode.fields import BBCodeTextField

# Project Imports
from users.models import User

# App Imports
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

    def __str__(self):
        return self.name

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        self.slug = slugify(self.basename).replace('_', '-')

        # TODO: Set the user_id based on the user that is logged in
        from random import choice
        if not self.user_id:
            self.user_id = choice(User.objects.all()).pk

        super(CommonBase, self).save(
                force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True
