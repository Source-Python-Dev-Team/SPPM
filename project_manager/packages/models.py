"""Package model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# App
from project_manager.common.models import (
    ProjectBase,
    ProjectContributor,
    ProjectGame,
    ProjectImage,
    ProjectRelease,
    ProjectTag,
)
from project_manager.common.validators import basename_validator
from .constants import PACKAGE_LOGO_URL
from .helpers import handle_package_image_upload
from .helpers import handle_package_logo_upload
from .helpers import handle_package_zip_upload


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'Package',
    'PackageContributor',
    'PackageGame',
    'PackageImage',
    'PackageRelease',
    'PackageTag',
)


# =============================================================================
# >> MODELS
# =============================================================================
class Package(ProjectBase):
    """Package project type model."""

    basename = models.CharField(
        max_length=32,
        validators=[basename_validator],
        unique=True,
        blank=True,
    )
    contributors = models.ManyToManyField(
        to='users.ForumUser',
        related_name='package_contributions',
        through='packages.PackageContributor',
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        blank=True,
        primary_key=True,
    )
    supported_games = models.ManyToManyField(
        to='games.Game',
        related_name='packages',
        through='packages.PackageGame',
    )
    tags = models.ManyToManyField(
        to='tags.Tag',
        related_name='packages',
        through='packages.PackageTag',
    )

    handle_logo_upload = handle_package_logo_upload

    def get_absolute_url(self):
        """Return the URL for the Package."""
        return reverse(
            viewname='packages:detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def save(self, *args, **kwargs):
        """Remove the old logo before storing the new one."""
        if self.logo and PACKAGE_LOGO_URL not in str(self.logo):
            path = settings.MEDIA_ROOT / PACKAGE_LOGO_URL
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.slug]
                if logo:
                    logo[0].remove()

        super().save(*args, **kwargs)


class PackageRelease(ProjectRelease):
    """Package release type model."""

    package = models.ForeignKey(
        to='packages.Package',
        related_name='releases',
    )

    handle_zip_file_upload = handle_package_zip_upload

    def get_absolute_url(self):
        """Return the URL for the PackageRelease."""
        return reverse(
            viewname='package-download',
            kwargs={
                'slug': self.package.slug,
                'zip_file': self.file_name,
            }
        )


class PackageImage(ProjectImage):
    """Package image type model."""

    package = models.ForeignKey(
        to='packages.Package',
        related_name='images',
    )

    handle_image_upload = handle_package_image_upload


class PackageContributor(ProjectContributor):
    """Package contributors through model."""

    package = models.ForeignKey(
        to='packages.Package',
    )

    class Meta:
        unique_together = ('package', 'user')


class PackageGame(ProjectGame):
    """Package supported_games through model."""

    package = models.ForeignKey(
        to='packages.Package',
    )

    class Meta:
        unique_together = ('package', 'game')


class PackageTag(ProjectTag):
    """Package tags through model."""

    package = models.ForeignKey(
        to='packages.Package',
    )

    class Meta:
        unique_together = ('package', 'tag')
