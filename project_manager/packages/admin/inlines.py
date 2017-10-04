"""Inline for Package admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.admin.inlines import (
    ProjectContributorInline,
    ProjectGameInline,
    ProjectTagInline,
)
from ..models import PackageContributor, PackageGame, PackageTag


# =============================================================================
# >> INLINES
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
