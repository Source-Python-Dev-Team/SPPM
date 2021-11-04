"""SubPlugin views."""

# =============================================================================
# IMPORTS
# =============================================================================
# App
from project_manager.common.mixins import DownloadMixin
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.constants import SUB_PLUGIN_RELEASE_URL
from project_manager.sub_plugins.models import SubPlugin, SubPluginRelease


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginReleaseDownloadView',
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
