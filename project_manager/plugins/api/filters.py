"""Plugin API filters."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.filters import ProjectFilter
from project_manager.plugins.models import Plugin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginFilter',
)


# =============================================================================
# >> FILTERS
# =============================================================================
class PluginFilter(ProjectFilter):
    """Filters for Plugins."""

    class Meta(ProjectFilter.Meta):
        """Define metaclass attributes."""

        model = Plugin
