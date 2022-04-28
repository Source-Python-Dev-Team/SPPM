"""SubPlugin views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Exists, OuterRef
from django.views.generic import TemplateView

# App
from project_manager.mixins import DownloadMixin
from project_manager.plugins.models import Plugin, SubPluginPath
from project_manager.sub_plugins.constants import SUB_PLUGIN_RELEASE_URL
from project_manager.sub_plugins.models import SubPlugin, SubPluginRelease


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginReleaseDownloadView',
    'SubPluginCreateView',
    'SubPluginView',
)


# =============================================================================
# VIEWS
# =============================================================================
class SubPluginReleaseDownloadView(DownloadMixin):
    """SubPlugin download view for releases."""

    model = SubPluginRelease
    project_model = Plugin
    model_kwarg = 'sub_plugin'
    base_url = SUB_PLUGIN_RELEASE_URL

    def get_instance(self, kwargs):
        """Return the project's instance."""
        instance = super().get_instance(kwargs)
        return SubPlugin.objects.get(**{
            'plugin': instance,
            'slug': self.kwargs.get('sub_plugin_slug'),
        })

    def get_base_path(self):
        """Return the base path for the download."""
        base_path = super().get_base_path()
        slug = self.kwargs.get('sub_plugin_slug')
        return base_path / slug


class SubPluginView(TemplateView):
    """Frontend view for viewing SubPlugins."""

    template_name = 'main.html'
    http_method_names = ('get', 'options')

    @staticmethod
    def _get_title(context):
        slug = context.get('slug')
        try:
            plugin = Plugin.objects.annotate(
                paths_exist=Exists(
                    queryset=SubPluginPath.objects.filter(
                        plugin_id=OuterRef('slug'),
                    )
                )
            ).get(slug=slug)
        except Plugin.DoesNotExist:
            return f'Plugin "{slug}" not found.'

        if not plugin.paths_exist:
            return f'Plugin "{plugin.name}" does not support sub-plugins.'

        sub_plugin_slug = context.get('sub_plugin_slug')
        if sub_plugin_slug is None:
            return f'SubPlugin Listing for {plugin.name}'

        try:
            sub_plugin = SubPlugin.objects.get(
                plugin=plugin,
                slug=sub_plugin_slug,
            )
            return f'{plugin.name} - {sub_plugin.name}'
        except SubPlugin.DoesNotExist:
            return f'SubPlugin "{sub_plugin_slug}" not found for Plugin "{plugin.name}".'

    def get_context_data(self, **kwargs):
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        context['title'] = self._get_title(context=context)
        return context


class SubPluginCreateView(TemplateView):
    """Frontend view for creating SubPlugins."""

    template_name = 'main.html'
    http_method_names = ('get', 'options')

    def get_context_data(self, **kwargs):
        """Add the page title to the context."""
        context = super().get_context_data(**kwargs)
        slug = context.get('slug')
        try:
            plugin = Plugin.objects.get(slug=slug)
            if not plugin.paths.exists():
                context['title'] = f'Plugin "{plugin.name}" does not support sub-plugins.'
            else:
                context['title'] = f'Create a SubPlugin for {plugin.name}'
        except Plugin.DoesNotExist:
            context['title'] = f'Plugin "{slug}" not found.'

        return context
