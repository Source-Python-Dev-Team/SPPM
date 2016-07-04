# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from __future__ import unicode_literals

# Django
from django.core.urlresolvers import reverse
from django.db import models

# App
from plugin_manager.common.validators import sub_plugin_path_validator


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginPath',
)


# =============================================================================
# >> MODELS
# =============================================================================
class SubPluginPath(models.Model):
    plugin = models.ForeignKey(
        to='plugin_manager.Plugin',
        related_name='paths',
    )
    path = models.CharField(
        max_length=256,
        validators=[sub_plugin_path_validator],
    )

    class Meta:
        verbose_name = 'SubPlugin path (Plugin)'
        verbose_name_plural = 'SubPlugin paths (Plugin)'
        unique_together = (
            'path', 'plugin',
        )

    def __str__(self):
        return self.path

    def get_absolute_url(self):
        return reverse(
            viewname='plugins:paths:list',
            kwargs={
                'slug': self.plugin.slug,
            }
        )
