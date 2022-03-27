"""Package model classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

# Third Party Django
from model_utils.fields import AutoCreatedField
from model_utils.tracker import FieldTracker

# App
from project_manager.common.constants import (
    PROJECT_BASENAME_MAX_LENGTH,
    PROJECT_SLUG_MAX_LENGTH,
    RELEASE_VERSION_MAX_LENGTH,
)
from project_manager.common.models import (
    AbstractUUIDPrimaryKeyModel,
    Project,
    ProjectRelease,
)
from project_manager.common.validators import (
    basename_validator,
    version_validator,
)
from project_manager.packages.constants import PACKAGE_LOGO_URL
from project_manager.packages.helpers import (
    handle_package_image_upload,
    handle_package_logo_upload,
    handle_package_zip_upload,
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

    class Meta:
        """Define metaclass attributes."""

        verbose_name = 'Package'
        verbose_name_plural = 'Packages'

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

    field_tracker = FieldTracker(
        fields=[
            'version',
        ]
    )

    @property
    def project(self):
        """Return the Package."""
        return self.package

    class Meta(ProjectRelease.Meta):
        """Define metaclass attributes."""

        unique_together = ('package', 'version')
        verbose_name = 'Package Release'
        verbose_name_plural = 'Package Releases'

    def get_absolute_url(self):
        """Return the URL for the PackageRelease."""
        return reverse(
            viewname='package-download',
            kwargs={
                'slug': self.package.slug,
                'zip_file': self.file_name,
            }
        )


class PackageImage(AbstractUUIDPrimaryKeyModel):
    """Package image type model."""

    package = models.ForeignKey(
        to='project_manager.Package',
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to=handle_package_image_upload,
    )
    created = AutoCreatedField(
        verbose_name='created',
    )

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class PackageContributor(AbstractUUIDPrimaryKeyModel):
    """Package contributors through model."""

    package = models.ForeignKey(
        to='project_manager.Package',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to='users.ForumUser',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package', 'user')

    @property
    def project(self):
        """Return the Package."""
        return self.package

    def __str__(self):
        """Return the base string."""
        return 'Package Contributor'

    def clean(self):
        """Validate that the package's owner cannot be a contributor."""
        if hasattr(self, 'user') and self.package.owner == self.user:
            raise ValidationError({
                'user': (
                    f'{self.user} is the owner and cannot be added '
                    f'as a contributor.'
                )
            })

        return super().clean()


class PackageGame(AbstractUUIDPrimaryKeyModel):
    """Package supported_games through model."""

    package = models.ForeignKey(
        to='project_manager.Package',
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        to='games.Game',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package', 'game')

    @property
    def project(self):
        """Return the Package."""
        return self.package

    def __str__(self):
        """Return the base string."""
        return 'Package Game'


class PackageTag(AbstractUUIDPrimaryKeyModel):
    """Package tags through model."""

    package = models.ForeignKey(
        to='project_manager.Package',
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        to='tags.Tag',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package', 'tag')

    @property
    def project(self):
        """Return the Package."""
        return self.package

    def __str__(self):
        """Return the base string."""
        return 'Package Tag'


class PackageReleaseDownloadRequirement(AbstractUUIDPrimaryKeyModel):
    """Package Download Requirement for Release model."""

    package_release = models.ForeignKey(
        to='project_manager.PackageRelease',
        on_delete=models.CASCADE,
    )
    download_requirement = models.ForeignKey(
        to='requirements.DownloadRequirement',
        on_delete=models.CASCADE,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package_release', 'download_requirement')

    def __str__(self):
        """Return the requirement's url."""
        return self.download_requirement.url


class PackageReleasePackageRequirement(AbstractUUIDPrimaryKeyModel):
    """Package Package Requirement for Release model."""

    package_release = models.ForeignKey(
        to='project_manager.PackageRelease',
        on_delete=models.CASCADE,
    )
    package_requirement = models.ForeignKey(
        to='project_manager.Package',
        on_delete=models.CASCADE,
    )
    version = models.CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        validators=[version_validator],
        help_text=(
            'The version of the custom package for this release '
            'of the package.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package_release', 'package_requirement')

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.package_requirement.name} - {self.version}'


class PackageReleasePyPiRequirement(AbstractUUIDPrimaryKeyModel):
    """Package PyPi Requirement for Release model."""

    package_release = models.ForeignKey(
        to='project_manager.PackageRelease',
        on_delete=models.CASCADE,
    )
    pypi_requirement = models.ForeignKey(
        to='requirements.PyPiRequirement',
        on_delete=models.CASCADE,
    )
    version = models.CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        validators=[version_validator],
        help_text=(
            'The version of the PyPi package for this release of the package.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package_release', 'pypi_requirement')

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.pypi_requirement.name} - {self.version}'


class PackageReleaseVersionControlRequirement(AbstractUUIDPrimaryKeyModel):
    """Package VCS Requirement for Release model."""

    package_release = models.ForeignKey(
        to='project_manager.PackageRelease',
        on_delete=models.CASCADE,
    )
    vcs_requirement = models.ForeignKey(
        to='requirements.VersionControlRequirement',
        on_delete=models.CASCADE,
    )
    version = models.CharField(
        max_length=RELEASE_VERSION_MAX_LENGTH,
        validators=[version_validator],
        help_text=(
            'The version of the VCS package for this release of the package.'
        ),
        blank=True,
        null=True,
    )
    optional = models.BooleanField(
        default=False,
    )

    class Meta:
        """Define metaclass attributes."""

        unique_together = ('package_release', 'vcs_requirement')

    def __str__(self):
        """Return the requirement's name and version."""
        return f'{self.vcs_requirement.url} - {self.version}'
