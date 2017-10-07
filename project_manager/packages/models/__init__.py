"""Package model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.urlresolvers import reverse
from django.db import models

# App
from project_manager.common.constants import (
    PROJECT_BASENAME_MAX_LENGTH,
    PROJECT_SLUG_MAX_LENGTH,
)
from project_manager.common.models import (
    ProjectBase,
    ProjectContributor,
    ProjectGame,
    ProjectImage,
    ProjectRelease,
    ProjectTag,
)
from project_manager.common.validators import basename_validator
from .abstract import PackageThroughBase
from ..constants import PACKAGE_LOGO_URL
from ..helpers import (
    handle_package_image_upload,
    handle_package_logo_upload,
    handle_package_zip_upload,
)


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
        max_length=PROJECT_BASENAME_MAX_LENGTH,
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
        max_length=PROJECT_SLUG_MAX_LENGTH,
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
    logo_path = PACKAGE_LOGO_URL

    def get_absolute_url(self):
        """Return the URL for the Package."""
        return reverse(
            viewname='packages:detail',
            kwargs={
                'slug': self.slug,
            }
        )


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


class PackageContributor(ProjectContributor, PackageThroughBase):
    """Package contributors through model."""

    class Meta:
        unique_together = ('package', 'user')


class PackageGame(ProjectGame, PackageThroughBase):
    """Package supported_games through model."""

    class Meta:
        unique_together = ('package', 'game')


class PackageTag(ProjectTag, PackageThroughBase):
    """Package tags through model."""

    class Meta:
        unique_together = ('package', 'tag')
