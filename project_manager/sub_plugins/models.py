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
from project_manager.common.models import CommonBase, Release
from project_manager.common.validators import (
    basename_validator, version_validator,
)
from project_manager.users.models import ForumUser
from .constants import SUB_PLUGIN_LOGO_URL
from .helpers import handle_sub_plugin_image_upload
from .helpers import handle_sub_plugin_logo_upload
from .helpers import handle_sub_plugin_zip_upload


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
class SubPlugin(CommonBase):
    name = models.CharField(
        max_length=64,
        help_text=(
            "The name of the sub-plugin. Do not include the version, as that "
            "is added dynamically to the sub-plugin's page."
        ),
    )
    basename = models.CharField(
        max_length=32,
        validators=[basename_validator],
        blank=True,
    )
    slug = models.SlugField(
        max_length=32,
        blank=True,
    )
    owner = models.ForeignKey(
        to='project_manager.ForumUser',
        related_name='sub_plugins',
    )
    contributors = models.ManyToManyField(
        to='project_manager.ForumUser',
        related_name='sub_plugin_contributions',
    )
    plugin = models.ForeignKey(
        to='project_manager.Plugin',
        related_name='sub_plugins',
    )
    package_requirements = models.ManyToManyField(
        to='project_manager.Package',
        related_name='required_in_sub_plugins',
    )
    pypi_requirements = models.ManyToManyField(
        to='project_manager.PyPiRequirement',
        related_name='required_in_sub_plugins',
    )
    logo = models.ImageField(
        upload_to=handle_sub_plugin_logo_upload,
        blank=True,
        null=True,
        help_text="The sub-plugin's logo image.",
    )
    supported_games = models.ManyToManyField(
        to='project_manager.Game',
        related_name='sub_plugins',
    )
    vcs_requirements = models.ManyToManyField(
        to='project_manager.VersionControlRequirement',
        related_name='sub_plugins',
    )
    download_requirements = models.ManyToManyField(
        to='project_manager.DownloadRequirement',
        related_name='sub_plugins',
    )

    class Meta:
        verbose_name = 'SubPlugin'
        verbose_name_plural = 'SubPlugins'
        unique_together = (
            ('plugin', 'basename'),
            ('plugin', 'name'),
            ('plugin', 'slug'),
        )

    def get_absolute_url(self):
        return reverse(
            viewname='plugins:sub-plugins:detail',
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
            path = settings.MEDIA_ROOT / SUB_PLUGIN_LOGO_URL
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
        to='project_manager.SubPlugin',
        related_name='releases',
    )
    version = models.CharField(
        max_length=8,
        validators=[version_validator],
        help_text='The version for this release of the sub-plugin.',
    )
    notes = BBCodeTextField(
        max_length=512,
        blank=True,
        null=True,
        help_text='The notes for this particular release of the sub-plugin.',
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
        to='project_manager.SubPlugin',
        related_name='images',
    )

    class Meta:
        verbose_name = 'Image (SubPlugin)'
        verbose_name_plural = 'Images (SubPlugin)'
