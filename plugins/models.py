from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

from common.models import CommonBase
from common.validators import sub_plugin_path_validator

from .helpers import handle_plugin_upload


__all__ = (
    'OldPluginRelease',
    'Plugin',
    'SubPluginPath',
)


# Create your models here.
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
        upload_to=handle_plugin_upload,
    )

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

        if self.current_version and self.current_zip_file:
            release = OldPluginRelease(
                version=self.current_version,
                zip_file=self.current_zip_file,
                plugin=self,
            )
            release.save()
        self.current_version = self.version
        self.current_zip_file = self.zip_file
        super(Plugin, self).save(
            force_insert, force_update, using, update_fields
        )


class SubPluginPath(models.Model):
    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='paths',
    )
    path = models.CharField(
        max_length=256,
        validators=[sub_plugin_path_validator],
    )


class OldPluginRelease(models.Model):
    version = models.CharField(
        max_length=8,
    )
    zip_file = models.FileField()
    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='previous_releases',
    )
