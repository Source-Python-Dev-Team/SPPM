"""Package model classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import reverse
from django.db import models

# App
from project_manager.common.constants import (
    PROJECT_BASENAME_MAX_LENGTH,
    PROJECT_SLUG_MAX_LENGTH,
)
from project_manager.common.models import (
    Project,
    ProjectContributor,
    ProjectGame,
    ProjectImage,
    ProjectRelease,
    ProjectReleaseDownloadRequirement,
    ProjectReleasePackageRequirement,
    ProjectReleasePyPiRequirement,
    ProjectReleaseVersionControlRequirement,
    ProjectTag,
)
from project_manager.common.validators import basename_validator
from project_manager.packages.constants import PACKAGE_LOGO_URL
from project_manager.packages.helpers import (
    handle_package_image_upload,
    handle_package_logo_upload,
    handle_package_zip_upload,
)
from project_manager.packages.models.abstract import (
    PackageReleaseThroughBase,
    PackageThroughBase,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'Package',
    'PackageContributor',
    'PackageGame',
    'PackageImage',
    'PackageRelease',
    'PackageReleaseDownloadRequirement',
    'PackageReleasePackageRequirement',
    'PackageReleasePyPiRequirement',
    'PackageReleaseVersionControlRequirement',
    'PackageTag',
)


# =============================================================================
# MODELS
# =============================================================================
class Package(Project):
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
        through='project_manager.PackageContributor',
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
        through='project_manager.PackageGame',
    )
    tags = models.ManyToManyField(
        to='tags.Tag',
        related_name='packages',
        through='project_manager.PackageTag',
    )

    handle_logo_upload = handle_package_logo_upload
    logo_path = PACKAGE_LOGO_URL

    def get_absolute_url(self):
        """Return the URL for the Package."""
        # TODO: add tests once this view is created
        return reverse(
            viewname='packages:detail',
            kwargs={
                'slug': self.slug,
            }
        )


class PackageRelease(ProjectRelease):
    """Package release type model."""

    package = models.ForeignKey(
        to='project_manager.Package',
        related_name='releases',
        on_delete=models.CASCADE,
    )
    download_requirements = models.ManyToManyField(
        to='requirements.DownloadRequirement',
        related_name='required_in_package_releases',
        through='project_manager.PackageReleaseDownloadRequirement',
    )
    package_requirements = models.ManyToManyField(
        to='project_manager.Package',
        related_name='required_in_package_releases',
        through='project_manager.PackageReleasePackageRequirement',
    )
    pypi_requirements = models.ManyToManyField(
        to='requirements.PyPiRequirement',
        related_name='required_in_package_releases',
        through='project_manager.PackageReleasePyPiRequirement',
    )
    vcs_requirements = models.ManyToManyField(
        to='requirements.VersionControlRequirement',
        related_name='required_in_package_releases',
        through='project_manager.PackageReleaseVersionControlRequirement',
    )

    handle_zip_file_upload = handle_package_zip_upload
    project_class = Package

    @property
    def project(self):
        """Return the Package."""
        return self.package

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
        to='project_manager.Package',
        related_name='images',
        on_delete=models.CASCADE,
    )

    handle_image_upload = handle_package_image_upload


class PackageContributor(PackageThroughBase, ProjectContributor):
    """Package contributors through model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package', 'user')


class PackageGame(ProjectGame, PackageThroughBase):
    """Package supported_games through model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package', 'game')


class PackageTag(ProjectTag, PackageThroughBase):
    """Package tags through model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package', 'tag')


class PackageReleaseDownloadRequirement(
    ProjectReleaseDownloadRequirement, PackageReleaseThroughBase
):
    """Package Download Requirement for Release model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package_release', 'download_requirement')


class PackageReleasePackageRequirement(
    ProjectReleasePackageRequirement, PackageReleaseThroughBase
):
    """Package Package Requirement for Release model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package_release', 'package_requirement')


class PackageReleasePyPiRequirement(
    ProjectReleasePyPiRequirement, PackageReleaseThroughBase
):
    """Package PyPi Requirement for Release model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package_release', 'pypi_requirement')


class PackageReleaseVersionControlRequirement(
    ProjectReleaseVersionControlRequirement, PackageReleaseThroughBase
):
    """Package VCS Requirement for Release model."""

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package_release', 'vcs_requirement')
