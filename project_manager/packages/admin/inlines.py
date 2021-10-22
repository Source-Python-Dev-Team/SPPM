"""Inline for Package admin classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# App
from project_manager.common.admin.inlines import (
    ProjectContributorInline,
    ProjectGameInline,
    ProjectImageInline,
    ProjectReleaseInline,
    ProjectTagInline,
)
from project_manager.packages.models import (
    PackageContributor,
    PackageGame,
    PackageImage,
    PackageRelease,
    PackageTag,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageContributorInline',
    'PackageGameInline',
    'PackageImageInline',
    'PackageReleaseInline',
    'PackageTagInline',
)


# =============================================================================
# INLINES
# =============================================================================
class PackageContributorInline(ProjectContributorInline):
    """Package Contributor Admin Inline."""

    model = PackageContributor


class PackageGameInline(ProjectGameInline):
    """Package Game Admin Inline."""

    model = PackageGame


class PackageTagInline(ProjectTagInline):
    """Package Tag Admin Inline."""

    model = PackageTag


class PackageImageInline(ProjectImageInline):
    """Package Image Inline."""

    model = PackageImage


class PackageReleaseInline(ProjectReleaseInline):
    """Package Release Inline."""

    model = PackageRelease
