"""SubPlugin model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.urlresolvers import reverse
from django.db import models

# App
from project_manager.common.models import (
    ProjectBase,
    ProjectContributor,
    ProjectGame,
    ProjectImage,
    ProjectRelease,
    ProjectTag,
)
from project_manager.common.validators import basename_validator
from .constants import SUB_PLUGIN_LOGO_URL
from .helpers import (
    handle_sub_plugin_image_upload,
    handle_sub_plugin_logo_upload,
    handle_sub_plugin_zip_upload,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPlugin',
    'SubPluginContributor',
    'SubPluginGame',
    'SubPluginImage',
    'SubPluginRelease',
    'SubPluginTag',
)


# =============================================================================
# >> MODELS
# =============================================================================
class SubPlugin(ProjectBase):
    """SubPlugin project type model."""

    id = models.CharField(
        max_length=65,
        blank=True,
        primary_key=True,
    )
    basename = models.CharField(
        max_length=32,
        validators=[basename_validator],
        blank=True,
    )
    contributors = models.ManyToManyField(
        to='users.ForumUser',
        related_name='subplugin_contributions',
        through='sub_plugins.SubPluginContributor',
    )
    slug = models.SlugField(
        max_length=32,
        blank=True,
    )
    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='sub_plugins',
    )
    supported_games = models.ManyToManyField(
        to='games.Game',
        related_name='subplugins',
        through='sub_plugins.SubPluginGame',
    )
    tags = models.ManyToManyField(
        to='tags.Tag',
        related_name='subplugins',
        through='sub_plugins.SubPluginTag',
    )

    handle_logo_upload = handle_sub_plugin_logo_upload
    logo_path = SUB_PLUGIN_LOGO_URL

    class Meta:
        verbose_name = 'SubPlugin'
        verbose_name_plural = 'SubPlugins'
        unique_together = (
            ('plugin', 'basename'),
            ('plugin', 'name'),
            ('plugin', 'slug'),
        )

    def __str__(self):
        """Return the string formatted name for the sub-plugin."""
        return f'{self.plugin.name}: {self.name}'

    def get_absolute_url(self):
        """Return the URL for the SubPlugin."""
        return reverse(
            viewname='plugins:sub-plugins:detail',
            kwargs={
                'slug': self.plugin.slug,
                'sub_plugin_slug': self.slug,
            }
        )

    def save(self, *args, **kwargs):
        """Set the id using the plugin's slug and the project's slug."""
        self.id = f'{self.plugin.slug}.{self.get_slug_value()}'
        super().save(*args, **kwargs)


class SubPluginRelease(ProjectRelease):
    """SubPlugin release type model."""

    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
        related_name='releases',
    )

    handle_zip_file_upload = handle_sub_plugin_zip_upload

    def get_absolute_url(self):
        """Return the URL for the SubPluginRelease."""
        return reverse(
            viewname='sub-plugin-download',
            kwargs={
                'slug': self.sub_plugin.plugin.slug,
                'sub_plugin_slug': self.sub_plugin.slug,
                'zip_file': self.file_name,
            }
        )


class SubPluginImage(ProjectImage):
    """SubPlugin image type model."""

    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
        related_name='images',
    )

    handle_image_upload = handle_sub_plugin_image_upload


class SubPluginContributor(ProjectContributor):
    """SubPlugin contributors through model."""

    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
    )

    class Meta:
        unique_together = ('sub_plugin', 'user')


class SubPluginGame(ProjectGame):
    """SubPlugin supported_games through model."""

    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
    )

    class Meta:
        unique_together = ('sub_plugin', 'game')


class SubPluginTag(ProjectTag):
    """SubPlugin tags through model."""

    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
    )

    class Meta:
        unique_together = ('sub_plugin', 'tag')
