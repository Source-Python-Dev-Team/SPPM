"""Package views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
from typing import Any

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
    "PackageCreateView",
    "PackageEditView",
    "PackageReleaseDownloadView",
    "PackageUpdateView",
    "PackageView",
)


# =============================================================================
# VIEWS
# =============================================================================
class PackageReleaseDownloadView(DownloadMixin):
    """Package download view for releases."""

    model = PackageRelease
    project_model = Package
    model_kwarg = "package"
    base_url = PACKAGE_RELEASE_URL


class PackageView(TemplateView):
    """Frontend view for viewing Packages."""

    template_name = "retrieve.html"
    http_method_names = ("get", "options")

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        slug = context.get("slug")
        if slug is None:
            context["title"] = "Package Listing"
        else:
            try:
                package = Package.objects.get(slug=slug)
                context["title"] = package.name
            except Package.DoesNotExist:
                context["title"] = f'Package "{slug}" not found.'
        return context


class PackageCreateView(TemplateView):
    """Frontend view for creating Packages."""

    template_name = "create.html"
    http_method_names = ("get", "options")

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Create a Package"
        return context


class PackageEditView(TemplateView):
    """Frontend view for editing Packages."""

    template_name = "edit.html"
    http_method_names = ("get", "options")

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        slug = context.get("slug")
        try:
            package = Package.objects.get(slug=slug)
            context["title"] = f"Edit {package.name}"
        except Package.DoesNotExist:
            context["title"] = f'Package "{slug}" not found.'
        return context


class PackageUpdateView(TemplateView):
    """Frontend view for updating Packages."""

    template_name = "update.html"
    http_method_names = ("get", "options")

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        slug = context.get("slug")
        try:
            package = Package.objects.get(slug=slug)
            context["title"] = f"Update {package.name}"
        except Package.DoesNotExist:
            context["title"] = f'Package "{slug}" not found.'
        return context
