"""Plugin model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# App
from project_manager.common.models import (
    AbstractUUIDPrimaryKeyModel,
    ProjectBase,
    ProjectContributor,
    ProjectGame,
    ProjectImage,
    ProjectRelease,
    ProjectTag,
)
from project_manager.common.validators import basename_validator
from .constants import PLUGIN_LOGO_URL
from .helpers import (
    handle_plugin_image_upload,
    handle_plugin_logo_upload,
    handle_plugin_zip_upload,
)


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
)


# =============================================================================
# >> MODELS
# =============================================================================
class Plugin(ProjectBase):
    """Plugin project type model."""

    basename = models.CharField(
        max_length=32,
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
        max_length=32,
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

    def get_absolute_url(self):
        """Return the URL for the Plugin."""
        return reverse(
            viewname='plugins:detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def save(self, *args, **kwargs):
        """Remove the old logo before storing the new one."""
        if self.logo and PLUGIN_LOGO_URL not in str(self.logo):
            path = settings.MEDIA_ROOT / PLUGIN_LOGO_URL
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.slug]
                if logo:
                    logo[0].remove()

        super().save(*args, **kwargs)


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


class PluginContributor(ProjectContributor):
    """Plugin contributors through model."""

    plugin = models.ForeignKey(
        to='plugins.Plugin',
    )

    class Meta:
        unique_together = ('plugin', 'user')


class PluginGame(ProjectGame):
    """Plugin supported_games through model."""

    plugin = models.ForeignKey(
        to='plugins.Plugin',
    )

    class Meta:
        unique_together = ('plugin', 'game')


class PluginTag(ProjectTag):
    """Plugin tags through model."""

    plugin = models.ForeignKey(
        to='plugins.Plugin',
    )

    class Meta:
        unique_together = ('plugin', 'tag')
