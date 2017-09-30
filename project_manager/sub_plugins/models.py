"""SubPlugin model classes."""

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
    ImageBase,
    ProjectBase,
    ReleaseBase,
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
    'SubPluginRelease',
    'SubPlugin',
    'SubPluginContributor',
    'SubPluginGame',
    'SubPluginImage',
    'SubPluginTag',
)


# =============================================================================
# >> MODELS
# =============================================================================
class SubPlugin(ProjectBase):
    """SubPlugin project type model."""

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

    class Meta:
        verbose_name = 'SubPlugin'
        verbose_name_plural = 'SubPlugins'
        unique_together = (
            ('plugin', 'basename'),
            ('plugin', 'name'),
            ('plugin', 'slug'),
        )

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
        """Remove the old logo before storing the new one."""
        if self.logo and SUB_PLUGIN_LOGO_URL not in str(self.logo):
            path = settings.MEDIA_ROOT / SUB_PLUGIN_LOGO_URL
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.slug]
                if logo:
                    logo[0].remove()

        super().save(*args, **kwargs)


class SubPluginRelease(ReleaseBase):
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


class SubPluginImage(ImageBase):
    """SubPlugin image type model."""

    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
        related_name='images',
    )

    handle_image_upload = handle_sub_plugin_image_upload


class SubPluginContributor(AbstractUUIDPrimaryKeyModel):
    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
    )
    user = models.ForeignKey(
        to='users.ForumUser',
    )

    class Meta:
        unique_together = ('sub_plugin', 'user')


class SubPluginGame(AbstractUUIDPrimaryKeyModel):
    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
    )
    game = models.ForeignKey(
        to='games.Game',
    )

    class Meta:
        unique_together = ('sub_plugin', 'game')


class SubPluginTag(AbstractUUIDPrimaryKeyModel):
    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
    )
    tag = models.ForeignKey(
        to='tags.Tag',
    )

    class Meta:
        unique_together = ('sub_plugin', 'tag')
