# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import unicode_literals

# Django Imports
from django.core.urlresolvers import reverse
from django.db import models

# 3rd-Party Django Imports
from precise_bbcode.fields import BBCodeTextField

# Project Imports
from common.models import CommonBase

# App Imports
from .helpers import handle_sub_plugin_image_upload
from .helpers import handle_sub_plugin_logo_upload
from .helpers import handle_sub_plugin_zip_upload


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'OldSubPluginRelease',
    'SubPlugin',
    'SubPluginImage',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
class OldSubPluginRelease(models.Model):
    version = models.CharField(
        max_length=8,
    )
    version_notes = BBCodeTextField(
        max_length=512,
        blank=True,
        null=True,
    )
    zip_file = models.FileField()
    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
        related_name='previous_releases',
    )


class SubPlugin(CommonBase):
    user = models.ForeignKey(
        to='users.User',
        related_name='sub_plugins',
    )
    contributors = models.ManyToManyField(
        to='users.User',
        related_name='sub_plugin_contributions',
    )
    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='sub_plugins',
    )
    package_requirements = models.ManyToManyField(
        to='packages.Package',
        related_name='required_in_sub_plugins',
    )
    pypi_requirements = models.ManyToManyField(
        to='pypi.PyPiRequirement',
        related_name='required_in_sub_plugins',
    )
    zip_file = models.FileField(
        upload_to=handle_sub_plugin_zip_upload,
    )
    logo = models.ImageField(
        upload_to=handle_sub_plugin_logo_upload,
        blank=True,
        null=True,
    )

    old_release_class = OldSubPluginRelease

    def get_absolute_url(self):
        return reverse(
            viewname='plugins:sub_plugins:sub_plugin_detail',
            kwargs={
                'slug': self.plugin.slug,
                'sub_plugin_slug': self.slug,
            }
        )


class SubPluginImage(models.Model):
    image = models.ImageField(
        upload_to=handle_sub_plugin_image_upload,
    )
    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
        related_name='images',
    )
