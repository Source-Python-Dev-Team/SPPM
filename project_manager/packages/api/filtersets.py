"""Package API filters."""

# =============================================================================
# IMPORTS
# =============================================================================
# App
from project_manager.api.common.filtersets import ProjectFilterSet
from project_manager.packages.models import Package


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageFilterSet',
)


# =============================================================================
# FILTERS
# =============================================================================
class PackageFilterSet(ProjectFilterSet):
    """Filters for Packages."""

    class Meta(ProjectFilterSet.Meta):
        """Define metaclass attributes."""

        model = Package
