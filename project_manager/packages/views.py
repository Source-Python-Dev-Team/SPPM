"""Package views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.views.generic import TemplateView

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
class PackageView(TemplateView):
    """View for Packages."""
    template_name = 'base.html'


class PackageReleaseDownloadView(DownloadMixin):
    """Package download view for releases."""

    model = PackageRelease
    super_model = Package
    super_kwarg = 'package'
    base_url = PACKAGE_RELEASE_URL
