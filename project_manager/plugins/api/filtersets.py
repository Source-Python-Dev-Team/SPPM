"""Plugin API filters."""

# =============================================================================
# IMPORTS
# =============================================================================
# App
from project_manager.common.api.filtersets import ProjectFilterSet
from project_manager.plugins.models import Plugin


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginFilterSet',
)


# =============================================================================
# FILTERS
# =============================================================================
class PluginFilterSet(ProjectFilterSet):
    """Filters for Plugins."""

    class Meta(ProjectFilterSet.Meta):
        """Define metaclass attributes."""

        model = Plugin
