"""Plugin model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.urlresolvers import reverse
from django.db import models

# App
from project_manager.common.constants import (
    PROJECT_BASENAME_MAX_LENGTH,
    PROJECT_SLUG_MAX_LENGTH,
)
from project_manager.common.models import (
    ProjectBase,
    ProjectContributor,
    ProjectGame,
    ProjectImage,
    ProjectRelease,
    ProjectTag,
)
from project_manager.common.validators import basename_validator
from .abstract import PluginThroughBase
from ..constants import PLUGIN_LOGO_URL, PATH_MAX_LENGTH
from ..helpers import (
    handle_plugin_image_upload,
    handle_plugin_logo_upload,
    handle_plugin_zip_upload,
)
from ..validators import sub_plugin_path_validator


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'Plugin',
    'PluginContributor',
    'PluginGame',
    'PluginImage',
    'PluginRelease',
    'PluginTag',
    'SubPluginPath',
)


# =============================================================================
# >> MODELS
# =============================================================================
class Plugin(ProjectBase):
    """Plugin project type model."""

    basename = models.CharField(
        max_length=PROJECT_BASENAME_MAX_LENGTH,
        validators=[basename_validator],
        unique=True,
        blank=True,
    )
    contributors = models.ManyToManyField(
        to='users.ForumUser',
        related_name='plugin_contributions',
        through='plugins.PluginContributor',
    )
    slug = models.SlugField(
        max_length=PROJECT_SLUG_MAX_LENGTH,
        unique=True,
        blank=True,
        primary_key=True,
    )
    supported_games = models.ManyToManyField(
        to='games.Game',
        related_name='plugins',
        through='plugins.PluginGame',
    )
    tags = models.ManyToManyField(
        to='tags.Tag',
        related_name='plugins',
        through='plugins.PluginTag',
    )

    handle_logo_upload = handle_plugin_logo_upload
    logo_path = PLUGIN_LOGO_URL

    def get_absolute_url(self):
        """Return the URL for the Plugin."""
        return reverse(
            viewname='plugins:detail',
            kwargs={
                'slug': self.slug,
            }
        )


class PluginRelease(ProjectRelease):
    """Plugin release type model."""

    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='releases',
    )

    handle_zip_file_upload = handle_plugin_zip_upload

    class Meta(ProjectRelease.Meta):
        unique_together = ('plugin', 'version')

    def get_absolute_url(self):
        """Return the URL for the PluginRelease."""
        return reverse(
            viewname='plugin-download',
            kwargs={
                'slug': self.plugin.slug,
                'zip_file': self.file_name,
            }
        )


class PluginImage(ProjectImage):
    """Plugin image type model."""

    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='images',
    )

    handle_image_upload = handle_plugin_image_upload


class PluginContributor(ProjectContributor, PluginThroughBase):
    """Plugin contributors through model."""

    class Meta:
        unique_together = ('plugin', 'user')


class PluginGame(ProjectGame, PluginThroughBase):
    """Plugin supported_games through model."""

    class Meta:
        unique_together = ('plugin', 'game')


class PluginTag(ProjectTag, PluginThroughBase):
    """Plugin tags through model."""

    class Meta:
        unique_together = ('plugin', 'tag')


class SubPluginPath(models.Model):
    """Model to store SubPlugin paths for a Plugin."""

    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='paths',
    )
    path = models.CharField(
        max_length=PATH_MAX_LENGTH,
        validators=[sub_plugin_path_validator],
    )

    class Meta:
        verbose_name = 'SubPlugin Path'
        verbose_name_plural = 'SubPlugin Paths'
        unique_together = (
            'path', 'plugin',
        )

    def __str__(self):
        """Return the path."""
        return self.path

    def get_absolute_url(self):
        """Return the SubPluginPath listing URL for the Plugin."""
        return reverse(
            viewname='plugins:paths:list',
            kwargs={
                'slug': self.plugin.slug,
            }
        )
