"""SubPlugin API filters."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.filters import ProjectFilter
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginFilter',
)


# =============================================================================
# >> FILTERS
# =============================================================================
class SubPluginFilter(ProjectFilter):
    """Filters for SubPlugins."""

    class Meta(ProjectFilter.Meta):
        """Define metaclass attributes."""

        model = SubPlugin
