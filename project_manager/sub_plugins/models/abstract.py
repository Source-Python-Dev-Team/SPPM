"""Base models for SubPlugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import models


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginThroughBase',
)


# =============================================================================
# >> MODELS
# =============================================================================
class SubPluginThroughBase(models.Model):
    """Base through model class for SubPlugins."""

    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
        on_delete=models.CASCADE,
    )

    @property
    def project(self):
        """Return the SubPlugin."""
        return self.sub_plugin

    class Meta:
        abstract = True
