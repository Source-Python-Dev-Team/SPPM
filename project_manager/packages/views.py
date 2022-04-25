"""Package views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.views.generic import TemplateView

# App
from project_manager.mixins import DownloadMixin
from project_manager.packages.constants import PACKAGE_RELEASE_URL
from project_manager.packages.models import Package, PackageRelease


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageReleaseDownloadView',
    'PackageCreateView',
    'PackageView',
)


# =============================================================================
# VIEWS
# =============================================================================
class PackageReleaseDownloadView(DownloadMixin):
    """Package download view for releases."""

    model = PackageRelease
    project_model = Package
    model_kwarg = 'package'
    base_url = PACKAGE_RELEASE_URL


class PackageView(TemplateView):
    """Frontend view for viewing Packages."""

    template_name = 'packages.html'
    http_method_names = ('get', 'options')

    def get_context_data(self, **kwargs):
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        slug = context.get('slug')
        if slug is None:
            context['title'] = 'Package Listing'
        else:
            try:
                package = Package.objects.get(slug=slug)
                context['title'] = package.name
            except Package.DoesNotExist:
                context['title'] = f'Package "{slug}" not found.'
        return context


class PackageCreateView(TemplateView):
    """Frontend view for creating Packages."""

    template_name = 'packages.html'
    http_method_names = ('get', 'options')

    def get_context_data(self, **kwargs):
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a Package'
        return context
