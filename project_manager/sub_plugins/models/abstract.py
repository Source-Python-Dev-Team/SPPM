"""Base models for SubPlugins."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import models


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginReleaseThroughBase',
    'SubPluginThroughBase',
)


# =============================================================================
# MODELS
# =============================================================================
class SubPluginThroughBase(models.Model):
    """Base through model class for SubPlugins."""

    sub_plugin = models.ForeignKey(
        to='project_manager.SubPlugin',
        on_delete=models.CASCADE,
    )

    @property
    def project(self):
        """Return the SubPlugin."""
        return self.sub_plugin

    class Meta:
        """Define metaclass attributes."""

        abstract = True


class SubPluginReleaseThroughBase(models.Model):
    """Base through model class for Packages."""

    sub_plugin_release = models.ForeignKey(
        to='project_manager.SubPluginRelease',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Define metaclass attributes."""

        abstract = True
