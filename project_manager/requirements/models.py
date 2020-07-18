"""Requirement model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify

# App
from project_manager.requirements.constants import (
    REQUIREMENT_NAME_MAX_LENGTH,
    REQUIREMENT_SLUG_MAX_LENGTH,
    REQUIREMENT_URL_MAX_LENGTH,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'DownloadRequirement',
    'PyPiRequirement',
    'VersionControlRequirement',
)


# =============================================================================
# >> MODELS
# =============================================================================
class DownloadRequirement(models.Model):
    """Download requirement model."""

    url = models.CharField(
        max_length=REQUIREMENT_URL_MAX_LENGTH,
    )

    class Meta:
        """Define metaclass attributes."""

        verbose_name = 'Download Requirement'
        verbose_name_plural = 'Download Requirements'


class PyPiRequirement(models.Model):
    """PyPi requirement model."""

    name = models.CharField(
        max_length=REQUIREMENT_NAME_MAX_LENGTH,
        unique=True,
    )
    slug = models.SlugField(
        max_length=REQUIREMENT_SLUG_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        """Define metaclass attributes."""

        verbose_name = 'PyPi Requirement'
        verbose_name_plural = 'PyPi Requirements'

    def __str__(self):
        """Return the object's name when str cast."""
        return str(self.name)

    def save(
        self, force_insert=False, force_update=False, using=None,
        update_fields=None
    ):
        """Set the slug and save the Requirement."""
        self.slug = slugify(self.name)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def get_absolute_url(self):
        """Return the URL for the PyPiRequirement."""
        return reverse(
            viewname='pypi:detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def get_pypi_url(self):
        """Return the PyPi URL for the requirement."""
        return settings.PYPI_URL + f'/{self.name}'


class VersionControlRequirement(models.Model):
    """VCS requirement model."""

    url = models.CharField(
        max_length=REQUIREMENT_URL_MAX_LENGTH,
    )

    class Meta:
        """Define metaclass attributes."""

        verbose_name = 'Version Control Requirement'
        verbose_name_plural = 'Version Control Requirements'
