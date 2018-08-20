"""Mixins for use with Plugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.plugins.models import Plugin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'RetrievePluginMixin',
)


# =============================================================================
# >> MIX-INS
# =============================================================================
class RetrievePluginMixin:
    """Mixin to retrieve the Plugin for the view."""

    _plugin = None

    @property
    def plugin(self):
        """Return the Plugin for the view."""
        if self._plugin is None:
            self._plugin = Plugin.objects.get(slug=self.kwargs['slug'])
        return self._plugin
