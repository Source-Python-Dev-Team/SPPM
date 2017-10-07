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
    'PluginThroughBase',
)


# =============================================================================
# >> MODELS
# =============================================================================
class PluginThroughBase(models.Model):
    """Base through model class for Plugins."""

    plugin = models.ForeignKey(
        to='plugins.Plugin',
    )

    @property
    def project(self):
        """Return the Plugin."""
        return self.plugin

    class Meta:
        abstract = True
