"""SubPlugin API filters."""

# =============================================================================
# IMPORTS
# =============================================================================
# App
from project_manager.common.api.filtersets import ProjectFilterSet
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginFilterSet',
)


# =============================================================================
# FILTERS
# =============================================================================
class SubPluginFilterSet(ProjectFilterSet):
    """Filters for SubPlugins."""

    class Meta(ProjectFilterSet.Meta):
        """Define metaclass attributes."""

        model = SubPlugin
