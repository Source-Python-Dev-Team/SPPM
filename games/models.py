"""Game model classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# App
from games.constants import (
    GAME_BASENAME_MAX_LENGTH,
    GAME_NAME_MAX_LENGTH,
    GAME_SLUG_MAX_LENGTH,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'Game',
)


# =============================================================================
# MODELS
# =============================================================================
class Game(models.Model):
    """Game model."""

    name = models.CharField(
        max_length=GAME_NAME_MAX_LENGTH,
        unique=True,
    )
    basename = models.CharField(
        max_length=GAME_BASENAME_MAX_LENGTH,
        unique=True,
    )
    slug = models.CharField(
        max_length=GAME_SLUG_MAX_LENGTH,
        unique=True,
        primary_key=True,
        blank=True,
    )
    icon = models.ImageField()

    class Meta:
        """Define metaclass attributes."""

        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        """Return the object's name when str cast."""
        return str(self.name)

    def save(self, *args, **kwargs):
        """Store the slug."""
        self.slug = slugify(self.basename).replace('_', '-')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the URL for the Game."""
        # TODO: add tests once this view is created
        return reverse(
            viewname='games:detail',
            kwargs={
                'slug': self.slug,
            }
        )
