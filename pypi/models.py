from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify

from SPPM.settings import PYPI_URL


__all__ = (
    'PyPiRequirement',
)


class PyPiRequirement(models.Model):

    name = models.CharField(
        max_length=32,
        unique=True,
    )

    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        self.slug = slugify(self.name)
        super(PyPiRequirement, self).save(
                force_insert, force_update, using, update_fields)

    def get_pypi_url(self):
        return PYPI_URL + '/{0}'.format(self.name)
