# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
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
# >> MODELS
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

    def save(self, *args, **kwargs):
        """Store the slug."""
        self.slug = slugify(self.basename)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            viewname='games:detail',
            kwargs={
                'slug': self.slug,
            }
        )
