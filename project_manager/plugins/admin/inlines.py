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
from ..models import PluginContributor, PluginGame, PluginTag


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
