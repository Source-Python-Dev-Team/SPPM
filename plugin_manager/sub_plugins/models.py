# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from __future__ import unicode_literals

# 3rd-Party Python
from path import Path

# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# App
from .constants import SUB_PLUGIN_LOGO_URL
from .helpers import handle_sub_plugin_image_upload
from .helpers import handle_sub_plugin_logo_upload
from .helpers import handle_sub_plugin_zip_upload
from ..common.models import CommonBase, Release
from ..users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginRelease',
    'SubPlugin',
    'SubPluginImage',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
class SubPlugin(CommonBase):
    owner = models.ForeignKey(
        to='plugin_manager.ForumUser',
        related_name='sub_plugins',
    )
    contributors = models.ManyToManyField(
        to='plugin_manager.ForumUser',
        related_name='sub_plugin_contributions',
    )
    plugin = models.ForeignKey(
        to='plugin_manager.Plugin',
        related_name='sub_plugins',
    )
    package_requirements = models.ManyToManyField(
        to='plugin_manager.Package',
        related_name='required_in_sub_plugins',
    )
    pypi_requirements = models.ManyToManyField(
        to='plugin_manager.PyPiRequirement',
        related_name='required_in_sub_plugins',
    )
    logo = models.ImageField(
        upload_to=handle_sub_plugin_logo_upload,
        blank=True,
        null=True,
    )
    supported_games = models.ManyToManyField(
        to='plugin_manager.Game',
        related_name='sub_plugins',
    )

    class Meta:
        verbose_name = 'SubPlugin'
        verbose_name_plural = 'SubPlugins'

    def get_absolute_url(self):
        return reverse(
            viewname='plugins:sub_plugins:detail',
            kwargs={
                'slug': self.plugin.slug,
                'sub_plugin_slug': self.slug,
            }
        )

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        """Remove the old logo before storing the new one."""
        if self.logo and SUB_PLUGIN_LOGO_URL not in str(self.logo):
            path = Path(settings.MEDIA_ROOT) / SUB_PLUGIN_LOGO_URL
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.slug]
                if logo:
                    logo[0].remove()

        # TODO: Set the owner based on the user that is logged in
        if not self.owner_id:
            from random import choice
            self.owner = choice(ForumUser.objects.all())

        super(SubPlugin, self).save(
            force_insert, force_update, using, update_fields)


class SubPluginRelease(Release):
    sub_plugin = models.ForeignKey(
        to='plugin_manager.SubPlugin',
        related_name='releases',
    )
    zip_file = models.FileField(
        upload_to=handle_sub_plugin_zip_upload,
    )

    class Meta:
        verbose_name = 'Release (SubPlugin)'
        verbose_name_plural = 'Releases (SubPlugin)'

    def get_absolute_url(self):
        return reverse(
            viewname='sub-plugin-download',
            kwargs={
                'slug': self.sub_plugin.plugin.slug,
                'sub_plugin_slug': self.sub_plugin.slug,
                'zip_file': self.file_name,
            }
        )


class SubPluginImage(models.Model):
    image = models.ImageField(
        upload_to=handle_sub_plugin_image_upload,
    )
    sub_plugin = models.ForeignKey(
        to='plugin_manager.SubPlugin',
        related_name='images',
    )

    class Meta:
        verbose_name = 'Image (SubPlugin)'
        verbose_name_plural = 'Images (SubPlugin)'
