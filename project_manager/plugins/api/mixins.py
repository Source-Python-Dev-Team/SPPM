"""Mixins for plugin functionalities between APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# App
from project_manager.plugins.helpers import get_plugin_basename
from project_manager.plugins.models import Plugin


# =============================================================================
# >> MIXINS
# =============================================================================
class PluginReleaseBase(object):
    """Serializer for listing Plugin releases."""

    project_class = Plugin
    project_type = 'plugin'

    @property
    def zip_parser(self):
        """Return the Plugin zip parsing function."""
        return get_plugin_basename

    def get_project_kwargs(self, parent_project=None):
        """Return kwargs for the project."""
        return {
            'pk': self.context['view'].kwargs.get('plugin_slug')
        }
