"""Plugin views."""
from typing import Any

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.views.generic import TemplateView

# App
from project_manager.mixins import DownloadMixin
from project_manager.plugins.constants import PLUGIN_RELEASE_URL
from project_manager.plugins.models import Plugin, PluginRelease

# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    "PluginCreateView",
    "PluginEditView",
    "PluginReleaseDownloadView",
    "PluginUpdateView",
    "PluginView",
)


# =============================================================================
# VIEWS
# =============================================================================
class PluginReleaseDownloadView(DownloadMixin):
    """Plugin download view for releases."""

    model = PluginRelease
    project_model = Plugin
    model_kwarg = "plugin"
    base_url = PLUGIN_RELEASE_URL


class PluginView(TemplateView):
    """Frontend view for viewing Plugins."""

    template_name = "retrieve.html"
    http_method_names = ("get", "options")

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        slug = context.get("slug")
        if slug is None:
            context["title"] = "Plugin Listing"
        else:
            try:
                plugin = Plugin.objects.get(slug=slug)
                context["title"] = plugin.name
            except Plugin.DoesNotExist:
                context["title"] = f'Plugin "{slug}" not found.'
        return context


class PluginCreateView(TemplateView):
    """Frontend view for creating Plugins."""

    template_name = "create.html"
    http_method_names = ("get", "options")

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Create a Plugin"
        return context


class PluginEditView(TemplateView):
    """Frontend view for editing Plugins."""

    template_name = "edit.html"
    http_method_names = ("get", "options")

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        slug = context.get("slug")
        try:
            plugin = Plugin.objects.get(slug=slug)
            context["title"] = f"Edit {plugin.name}"
        except Plugin.DoesNotExist:
            context["title"] = f'Plugin "{slug}" not found.'
        return context


class PluginUpdateView(TemplateView):
    """Frontend view for updating Plugins."""

    template_name = "update.html"
    http_method_names = ("get", "options")

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        slug = context.get("slug")
        try:
            plugin = Plugin.objects.get(slug=slug)
            context["title"] = f"Update {plugin.name}"
        except Plugin.DoesNotExist:
            context["title"] = f'Plugin "{slug}" not found.'
        return context
