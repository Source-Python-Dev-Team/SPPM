"""Inline for SubPlugin admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.admin.inlines import (
    ProjectContributorInline,
    ProjectGameInline,
    ProjectTagInline,
)
from project_manager.sub_plugins.models import (
    SubPluginContributor,
    SubPluginGame,
    SubPluginTag,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginContributorInline',
    'SubPluginGameInline',
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
