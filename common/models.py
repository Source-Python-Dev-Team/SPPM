from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify

from users.models import User

from .validators import basename_validator, version_validator


__all__ = (
    'CommonBase',
    'readable_data_file_types',
)


readable_data_file_types = [
    'json',
    'ini',
    'res',
    'txt',
    'vdf',
    'xml',
]


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
    current_zip_file = models.FileField(
        blank=True,
        null=True,
    )

    allowed_file_types = {
        'cfg/source-python/': [
            'cfg',
            'ini',
            'md',
        ],

        'log/source-python/': [
            'md',
            'txt',
        ],

        'models/': [
            'ani',
            'mdl',
            'phy',
            'vmf',
            'vmx',
            'vtf',
            'vtx',
            'vvd',
        ],

        'particles/': [
            'pcf',
            'txt',
        ],

        'resource/source-python/events/': [
            'md',
            'res',
            'txt',
        ],

        'resource/source-python/translations/': [
            'md',
            'ini',
        ],

        'sound/source-python/': [
            'mp3',
            'ogg',
            'wav',
        ],
    }

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
