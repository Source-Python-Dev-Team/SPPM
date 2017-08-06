"""SubPlugin model classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# App
from project_manager.common.models import ImageBase, ProjectBase, ReleaseBase
from project_manager.common.validators import basename_validator
from project_manager.users.models import ForumUser
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
    'SubPluginImage',
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
    slug = models.SlugField(
        max_length=32,
        blank=True,
    )
    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='sub_plugins',
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

        # TODO: Set the owner based on the user that is logged in
        if not self.owner_id:
            from random import choice
            self.owner = choice(ForumUser.objects.all())

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
