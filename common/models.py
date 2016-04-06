from __future__ import unicode_literals

from zipfile import ZipFile

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
    """"""

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
    )

    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    date_created = models.DateTimeField(
        'date created',
        auto_now_add=True,
    )

    zip_file = models.FileField()

    can_install = models.NullBooleanField()

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

    date_last_updated = models.DateTimeField(
        'date last updated',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        # TODO: Validate the zip file
        self.validate_zip_file()

        # TODO: Set the user_id based on the user that is logged in
        from random import choice
        self.user_id = choice(User.objects.all()).pk
        return super(CommonBase, self).clean_fields()

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        self.slug = slugify(self.basename)
        super(CommonBase, self).save(
                force_insert, force_update, using, update_fields)

    def validate_zip_file(self):
        zip_file = ZipFile(self.zip_file)
        self.basename = self.get_basename(zip_file)
        self.validate_file_types(zip_file)

    def get_basename(self, zip_file):
        raise NotImplementedError

    def validate_file_types(self, zip_file):
        pass

    class Meta:
        abstract = True
