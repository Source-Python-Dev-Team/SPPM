"""Base models for Plugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import models


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginReleaseThroughBase',
    'PluginThroughBase',
)


# =============================================================================
# >> MODELS
# =============================================================================
class PluginThroughBase(models.Model):
    """Base through model class for Plugins."""

    plugin = models.ForeignKey(
        to='plugins.Plugin',
        on_delete=models.CASCADE,
    )

    @property
    def project(self):
        """Return the Plugin."""
        return self.plugin

    class Meta:
        """Define metaclass attributes."""

        abstract = True


class PluginReleaseThroughBase(models.Model):
    """Base through model class for Packages."""

    plugin_release = models.ForeignKey(
        to='plugins.PluginRelease',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True
