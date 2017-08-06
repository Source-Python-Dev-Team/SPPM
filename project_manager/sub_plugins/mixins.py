"""Mixins for use with SubPlugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.plugins.mixins import RetrievePluginMixin
from .models import SubPlugin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'RetrieveSubPluginMixin',
)


# =============================================================================
# >> MIX-INS
# =============================================================================
class RetrieveSubPluginMixin(RetrievePluginMixin):
    """Mixin to retrieve the SubPlugin for the view."""

    _sub_plugin = None

    @property
    def sub_plugin(self):
        """Return the SubPlugin for the view."""
        if self._sub_plugin is None:
            self._sub_plugin = SubPlugin.objects.get(
                plugin=self.plugin,
                slug=self.kwargs['sub_plugin_slug']
            )
        return self._sub_plugin
