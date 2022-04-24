"""Plugin views."""

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
    'PluginReleaseDownloadView',
    'PluginCreateView',
    'PluginView',
)


# =============================================================================
# VIEWS
# =============================================================================
class PluginReleaseDownloadView(DownloadMixin):
    """Plugin download view for releases."""

    model = PluginRelease
    project_model = Plugin
    model_kwarg = 'plugin'
    base_url = PLUGIN_RELEASE_URL


class PluginView(TemplateView):
    """Frontend view for viewing Plugins."""

    template_name = 'plugins.html'
    http_method_names = ('get', 'options')

    def get_context_data(self, **kwargs):
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        slug = context.get('slug')
        if slug is None:
            context['title'] = 'Plugin Listing'
        else:
            try:
                plugin = Plugin.objects.get(slug=slug)
                context['title'] = plugin.name
            except Plugin.DoesNotExist:
                context['title'] = f'Plugin "{slug}" not found.'
        return context


class PluginCreateView(TemplateView):
    """Frontend view for creating Plugins."""

    template_name = 'plugins.html'
    http_method_names = ('get', 'post', 'options')

    def get_context_data(self, **kwargs):
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a Plugin'
        return context
