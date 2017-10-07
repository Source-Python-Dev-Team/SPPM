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
    'PackageThroughBase',
)


# =============================================================================
# >> MODELS
# =============================================================================
class PackageThroughBase(models.Model):
    """Base through model class for Packages."""

    package = models.ForeignKey(
        to='packages.Package',
    )

    @property
    def project(self):
        """Return the Package."""
        return self.package

    class Meta:
        abstract = True
