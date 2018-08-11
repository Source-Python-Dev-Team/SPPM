"""Base models for Packages."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import models


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageReleaseThroughBase',
    'PackageThroughBase',
)


# =============================================================================
# >> MODELS
# =============================================================================
class PackageThroughBase(models.Model):
    """Base through model class for Packages."""

    package = models.ForeignKey(
        to='packages.Package',
        on_delete=models.CASCADE,
    )

    @property
    def project(self):
        """Return the Package."""
        return self.package

    class Meta:
        abstract = True


class PackageReleaseThroughBase(models.Model):
    """Base through model class for Packages."""

    package_release = models.ForeignKey(
        to='packages.PackageRelease',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
