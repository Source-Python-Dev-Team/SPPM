"""Mixins for sub-plugin functionalities between APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# App
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.helpers import get_sub_plugin_basename
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginReleaseBase',
)


# =============================================================================
# >> MIXINS
# =============================================================================
class SubPluginReleaseBase(object):
    """Serializer for listing Plugin releases."""

    project_class = SubPlugin
    project_type = 'sub-plugin'

    @property
    def parent_project(self):
        """Return the parent plugin."""
        kwargs = self.context['view'].kwargs
        plugin_slug = kwargs.get('plugin_slug')
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
        except Plugin.DoesNotExist:
            raise ValidationError(f"Plugin '{plugin_slug}' not found.")
        return plugin

    @property
    def zip_parser(self):
        """Return the SubPlugin zip parsing function."""
        return get_sub_plugin_basename

    def get_project_kwargs(self, parent_project=None):
        """Return kwargs for the project."""
        kwargs = self.context['view'].kwargs
        return {
            'slug': kwargs.get('sub_plugin_slug'),
            'plugin': parent_project,
        }
