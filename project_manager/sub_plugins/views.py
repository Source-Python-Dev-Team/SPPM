"""SubPlugin views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.mixins import DownloadMixin
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.constants import SUB_PLUGIN_RELEASE_URL
from project_manager.sub_plugins.models import SubPlugin, SubPluginRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginReleaseDownloadView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class SubPluginReleaseDownloadView(DownloadMixin):
    """SubPlugin download view for releases."""

    model = SubPluginRelease
    super_model = Plugin
    sub_model = SubPlugin
    slug_url_kwarg = 'sub_plugin_slug'
    super_kwarg = 'plugin'
    sub_kwarg = 'sub_plugin'
    base_url = SUB_PLUGIN_RELEASE_URL
