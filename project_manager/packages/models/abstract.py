"""Base models for Packages."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageReleaseThroughBase',
    'PackageThroughBase',
)


# =============================================================================
# MODELS
# =============================================================================
class PackageThroughBase(models.Model):
    """Base through model class for Packages."""

    package = models.ForeignKey(
        to='project_manager.Package',
        on_delete=models.CASCADE,
    )

    @property
    def project(self):
        """Return the Package."""
        return self.package

    class Meta:
        """Define metaclass attributes."""

        abstract = True


class PackageReleaseThroughBase(models.Model):
    """Base through model class for Packages."""

    package_release = models.ForeignKey(
        to='project_manager.PackageRelease',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True
