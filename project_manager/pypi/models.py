# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from __future__ import unicode_literals

# Django
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
# >> MODELS
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

    class Meta:
        verbose_name = 'PyPi Requirement'
        verbose_name_plural = 'PyPi Requirements'

    def __str__(self):
        """Return the object's name when str cast."""
        return self.name

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        self.slug = slugify(self.name).replace('_', '-')
        super(PyPiRequirement, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )

    def get_absolute_url(self):
        return reverse(
            viewname='pypi:detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def get_pypi_url(self):
        return settings.PYPI_URL + '/{name}'.format(name=self.name)
