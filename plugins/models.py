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

# 3rd-Party Django Imports
from precise_bbcode.fields import BBCodeTextField

# Project Imports
from common.models import CommonBase
from common.validators import sub_plugin_path_validator

# App Imports
from .helpers import handle_plugin_image_upload
from .helpers import handle_plugin_logo_upload
from .helpers import handle_plugin_zip_upload


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'OldPluginRelease',
    'Plugin',
    'SubPluginPath',
)


# =============================================================================
# >> MODEL CLASSES
# =============================================================================
class OldPluginRelease(models.Model):
    version = models.CharField(
        max_length=8,
    )
    version_notes = BBCodeTextField(
        max_length=512,
        blank=True,
        null=True,
    )
    zip_file = models.FileField()
    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='previous_releases',
    )


class Plugin(CommonBase):
    user = models.ForeignKey(
        to='users.User',
        related_name='plugins',
    )
    contributors = models.ManyToManyField(
        to='users.User',
        related_name='plugin_contributions',
    )
    package_requirements = models.ManyToManyField(
        to='packages.Package',
        related_name='required_in_plugins',
    )
    pypi_requirements = models.ManyToManyField(
        to='pypi.PyPiRequirement',
        related_name='required_in_plugins',
    )
    zip_file = models.FileField(
        upload_to=handle_plugin_zip_upload,
    )
    logo = models.ImageField(
        upload_to=handle_plugin_logo_upload,
        blank=True,
        null=True,
    )

    old_release_class = OldPluginRelease

    def get_absolute_url(self):
        return reverse(
            viewname='plugins:plugin_detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        """Remove the old logo before storing the new one."""
        if self.logo and u'logo/' not in self.logo:
            path = Path(settings.MEDIA_ROOT) / 'logos' / 'plugins'
            if path.isdir():
                logo = [x for x in path.files() if x.namebase == self.basename]
                if logo:
                    logo[0].remove()

        super(Plugin, self).save(
            force_insert, force_update, using, update_fields)


class SubPluginPath(models.Model):
    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='paths',
    )
    path = models.CharField(
        max_length=256,
        validators=[sub_plugin_path_validator],
    )


class PluginImage(models.Model):
    image = models.ImageField(
        upload_to=handle_plugin_image_upload,
    )
    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='images',
    )
