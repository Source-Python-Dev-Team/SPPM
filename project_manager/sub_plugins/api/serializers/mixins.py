"""Mixins for sub-plugin functionalities between APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.utils.functional import cached_property

# Third Party Django
from rest_framework.exceptions import ValidationError

# App
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.helpers import SubPluginZipFile
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginReleaseBase',
)


# =============================================================================
# MIXINS
# =============================================================================
class SubPluginReleaseBase:
    """Serializer for listing Plugin releases."""

    project_class = SubPlugin
    project_type = 'sub-plugin'

    @cached_property
    def parent_project(self):
        """Return the parent plugin."""
        kwargs = getattr(self, 'context')['view'].kwargs
        plugin_slug = kwargs.get('plugin_slug')
        try:
            plugin = Plugin.objects.get(slug=plugin_slug)
        except Plugin.DoesNotExist as exception:
            raise ValidationError(
                f"Plugin '{plugin_slug}' not found."
            ) from exception
        return plugin

    @property
    def zip_parser(self):
        """Return the SubPlugin zip parsing function."""
        return SubPluginZipFile

    def get_project_kwargs(self):
        """Return kwargs for the project."""
        kwargs = getattr(self, 'context')['view'].kwargs
        return {
            'slug': kwargs.get('sub_plugin_slug'),
            'plugin': self.parent_project,
        }
