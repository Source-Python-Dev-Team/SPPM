"""Inline for SubPlugin admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.admin.inlines import (
    ProjectContributorInline,
    ProjectGameInline,
    ProjectImageInline,
    ProjectReleaseInline,
    ProjectTagInline,
)
from project_manager.sub_plugins.models import (
    SubPluginContributor,
    SubPluginGame,
    SubPluginImage,
    SubPluginRelease,
    SubPluginTag,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginContributorInline',
    'SubPluginGameInline',
    'SubPluginImageInline',
    'SubPluginReleaseInline',
    'SubPluginTagInline',
)


# =============================================================================
# >> INLINES
# =============================================================================
class SubPluginContributorInline(ProjectContributorInline):
    """SubPlugin Contributor Admin Inline."""

    model = SubPluginContributor


class SubPluginGameInline(ProjectGameInline):
    """SubPlugin Game Admin Inline."""

    model = SubPluginGame


class SubPluginTagInline(ProjectTagInline):
    """SubPlugin Tag Admin Inline."""

    model = SubPluginTag


class SubPluginImageInline(ProjectImageInline):
    """Plugin Image Inline."""

    model = SubPluginImage


class SubPluginReleaseInline(ProjectReleaseInline):
    """Plugin Release Inline."""

    model = SubPluginRelease
