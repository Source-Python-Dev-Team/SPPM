# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify


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
    name = models.CharField(
        max_length=64,
    )
    url = models.CharField(
        max_length=128,
    )
    description = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Download Requirement'
        verbose_name_plural = 'Download Requirements'


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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            viewname='pypi:detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def get_pypi_url(self):
        return settings.PYPI_URL + f'/{self.name}'


class VersionControlRequirement(models.Model):
    GIT = 0
    MERCURIAL = 1
    SUBVERSION = 2
    BAZAAR = 3

    SUPPORTED_VCS_TYPES = {
        GIT: 'git',
        MERCURIAL: 'hg',
        SUBVERSION: 'svn',
        BAZAAR: 'bzr',
    }

    name = models.CharField(
        max_length=64,
    )
    vcs_type = models.PositiveSmallIntegerField(
        choices=tuple(SUPPORTED_VCS_TYPES.items()),
        help_text='The type of Version Control used in the url.',
        db_index=True,
        editable=False,
        null=True,
    )
    url = models.CharField(
        max_length=128,
    )

    class Meta:
        verbose_name = 'Version Control Requirement'
        verbose_name_plural = 'Version Control Requirements'
