# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from __future__ import unicode_literals

# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# 3rd-Party Django
from precise_bbcode.fields import BBCodeTextField

# App
from plugin_manager.common.models import CommonBase, Release
from plugin_manager.common.validators import (
    basename_validator, version_validator,
)
from plugin_manager.users.models import ForumUser
from .constants import PLUGIN_LOGO_URL
from .helpers import handle_plugin_image_upload
from .helpers import handle_plugin_logo_upload
from .helpers import handle_plugin_zip_upload


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginRelease',
    'Plugin',
    'PluginImage',
)


# =============================================================================
# >> MODELS
# =============================================================================
class Plugin(CommonBase):
    name = models.CharField(
        max_length=64,
        unique=True,
        help_text=(
            "The name of the plugin. Do not include the version, as that is "
            "added dynamically to the plugin's page."
        ),
    )
    basename = models.CharField(
        max_length=32,
        validators=[basename_validator],
        unique=True,
        blank=True,
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        blank=True,
    )
    owner = models.ForeignKey(
        to='plugin_manager.ForumUser',
        related_name='plugins',
    )
    contributors = models.ManyToManyField(
        to='plugin_manager.ForumUser',
        related_name='plugin_contributions',
    )
    package_requirements = models.ManyToManyField(
        to='plugin_manager.Package',
        related_name='required_in_plugins',
    )
    pypi_requirements = models.ManyToManyField(
        to='plugin_manager.PyPiRequirement',
        related_name='required_in_plugins',
    )
    logo = models.ImageField(
        upload_to=handle_plugin_logo_upload,
        blank=True,
        null=True,
        help_text="The plugin's logo image.",
    )
    supported_games = models.ManyToManyField(
        to='plugin_manager.Game',
        related_name='plugins',
    )
    vcs_requirements = models.ManyToManyField(
        to='plugin_manager.VersionControlRequirement',
        related_name='plugins',
    )
    download_requirements = models.ManyToManyField(
        to='plugin_manager.DownloadRequirement',
        related_name='plugins',
    )

    def get_absolute_url(self):
        return reverse(
            viewname='plugins:detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        """Remove the old logo before storing the new one."""
        if self.logo and PLUGIN_LOGO_URL not in str(self.logo):
            path = settings.MEDIA_ROOT / PLUGIN_LOGO_URL
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.slug]
                if logo:
                    logo[0].remove()

        # TODO: Set the owner based on the user that is logged in
        if not self.owner_id:
            from random import choice
            self.owner = choice(ForumUser.objects.all())

        super(Plugin, self).save(
            force_insert, force_update, using, update_fields)


class PluginRelease(Release):
    plugin = models.ForeignKey(
        to='plugin_manager.Plugin',
        related_name='releases',
    )
    version = models.CharField(
        max_length=8,
        validators=[version_validator],
        help_text='The version for this release of the plugin.',
    )
    notes = BBCodeTextField(
        max_length=512,
        blank=True,
        null=True,
        help_text='The notes for this particular release of the plugin.',
    )
    zip_file = models.FileField(
        upload_to=handle_plugin_zip_upload,
    )

    class Meta:
        verbose_name = 'Release (Plugin)'
        verbose_name_plural = 'Releases (Plugin)'

    def get_absolute_url(self):
        return reverse(
            viewname='plugin-download',
            kwargs={
                'slug': self.plugin.slug,
                'zip_file': self.file_name,
            }
        )


class PluginImage(models.Model):
    image = models.ImageField(
        upload_to=handle_plugin_image_upload,
    )
    plugin = models.ForeignKey(
        to='plugin_manager.Plugin',
        related_name='images',
    )

    class Meta:
        verbose_name = 'Image (Plugin)'
        verbose_name_plural = 'Images (Plugin)'
