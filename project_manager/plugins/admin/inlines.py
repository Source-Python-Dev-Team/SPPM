"""Inline for Plugin admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.admin.inlines import (
    ProjectContributorInline,
    ProjectGameInline,
    ProjectTagInline,
)
from project_manager.plugins.models import (
    PluginContributor,
    PluginGame,
    PluginTag,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginContributorInline',
    'PluginGameInline',
    'PluginTagInline',
)


# =============================================================================
# >> INLINES
# =============================================================================
class PluginContributorInline(ProjectContributorInline):
    """Plugin Contributor Admin Inline."""

    model = PluginContributor


class PluginGameInline(ProjectGameInline):
    """Plugin Game Admin Inline."""

    model = PluginGame


class PluginTagInline(ProjectTagInline):
    """Plugin Tag Admin Inline."""

    model = PluginTag
