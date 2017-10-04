"""Package API filters."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.api.filters import ProjectFilter
from ..models import Package


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageFilter',
)


# =============================================================================
# >> FILTERS
# =============================================================================
class PackageFilter(ProjectFilter):
    """Filters for Packages."""

    class Meta(ProjectFilter.Meta):
        model = Package
