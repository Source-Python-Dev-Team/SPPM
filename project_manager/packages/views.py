"""Package views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.mixins import DownloadMixin
from project_manager.packages.constants import PACKAGE_RELEASE_URL
from project_manager.packages.models import Package, PackageRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageReleaseDownloadView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PackageReleaseDownloadView(DownloadMixin):
    """Package download view for releases."""

    model = PackageRelease
    project_model = Package
    model_kwarg = 'package'
    base_url = PACKAGE_RELEASE_URL
