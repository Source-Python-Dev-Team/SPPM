# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import unicode_literals

# 3rd-Party Python
from path import Path

# Django Imports
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now

# 3rd-Party Django Imports
from precise_bbcode.fields import BBCodeTextField

# Project Imports
from ..common.models import CommonBase

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
class SubPlugin(CommonBase):
    owner = models.ForeignKey(
        to='SPPM.ForumUser',
        related_name='sub_plugins',
    )
    contributors = models.ManyToManyField(
        to='SPPM.ForumUser',
        related_name='sub_plugin_contributions',
    )
    plugin = models.ForeignKey(
        to='SPPM.Plugin',
        related_name='sub_plugins',
    )
    package_requirements = models.ManyToManyField(
        to='SPPM.Package',
        related_name='required_in_sub_plugins',
    )
    pypi_requirements = models.ManyToManyField(
        to='SPPM.PyPiRequirement',
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
    supported_games = models.ManyToManyField(
        to='SPPM.Game',
        related_name='sub_plugins',
    )

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
        if self.logo and u'logo/' not in self.logo:
            path = Path(settings.MEDIA_ROOT) / 'logos' / 'sub_plugins'
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.basename]
                if logo:
                    logo[0].remove()

        release = None

        if self.current_version and self.current_version != self.version:
            release = OldSubPluginRelease(
                version=self.current_version,
                version_notes=self.current_version_notes,
                zip_file=self.current_zip_file,
                sub_plugin=self,
            )
            self.date_last_updated = now()

        self.current_version = self.version
        self.current_version_notes = self.version_notes
        self.current_zip_file = self.zip_file

        super(SubPlugin, self).save(
            force_insert, force_update, using, update_fields)

        if release is not None:
            release.save()
            self.previous_releases.add(release)


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
        to='SPPM.SubPlugin',
        related_name='previous_releases',
    )


class SubPluginImage(models.Model):
    image = models.ImageField(
        upload_to=handle_sub_plugin_image_upload,
    )
    sub_plugin = models.ForeignKey(
        to='SPPM.SubPlugin',
        related_name='images',
    )
