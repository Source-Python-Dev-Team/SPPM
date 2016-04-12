# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import unicode_literals

# Django Imports
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PyPiRequirement',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
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
        self.slug = slugify(self.name).replace('_', '-')
        super(PyPiRequirement, self).save(
                force_insert, force_update, using, update_fields)

    def get_absolute_url(self):
        return reverse(
            viewname='pypi:pypi_detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def get_pypi_url(self):
        return settings.PYPI_URL + '/{0}'.format(self.name)
