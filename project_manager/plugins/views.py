"""Plugin views."""

# =============================================================================
# IMPORTS
# =============================================================================
# App
from project_manager.common.mixins import DownloadMixin
from project_manager.plugins.constants import PLUGIN_RELEASE_URL
from project_manager.plugins.models import Plugin, PluginRelease


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginReleaseDownloadView',
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
