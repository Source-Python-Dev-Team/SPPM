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
from .helpers import handle_sub_plugin_upload


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'OldSubPluginRelease',
    'SubPlugin',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
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
        upload_to=handle_sub_plugin_upload,
    )

    def get_absolute_url(self):
        return reverse(
            viewname='plugins:sub_plugins:sub_plugin_detail',
            kwargs={
                'slug': self.plugin.slug,
                'sub_plugin_slug': self.slug,
            }
        )

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        if self.current_version and self.current_zip_file:
            release = OldSubPluginRelease(
                version=self.current_version,
                zip_file=self.current_zip_file,
            )
            self.previous_releases.add(release)
        self.current_version = self.version
        self.current_version_notes = self.version_notes
        self.current_zip_file = self.zip_file
        super(SubPlugin, self).save(
            force_insert, force_update, using, update_fields
        )


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
