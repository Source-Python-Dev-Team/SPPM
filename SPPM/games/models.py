# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import unicode_literals

# Django Imports
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'Game',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
class Game(models.Model):
    name = models.CharField(
        max_length=16,
        unique=True,
    )
    basename = models.CharField(
        max_length=16,
        unique=True,
    )
    slug = models.CharField(
        max_length=16,
        unique=True,
        blank=True,
    )
    icon = models.ImageField()

    def __str__(self):
        """Return the object's name when str cast."""
        return self.name

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        """Store the slug."""
        self.slug = slugify(self.basename).replace('_', '-')
        super(Game, self).save(
            force_insert, force_update, using, update_fields)

    def get_absolute_url(self):
        return reverse(
            viewname='games:detail',
            kwargs={
                'slug': self.slug,
            }
        )
