"""SubPlugin API filters."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.filters import ProjectFilter
from ..models import SubPlugin


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
        model = SubPlugin
