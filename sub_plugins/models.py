from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

from common.models import CommonBase, readable_data_file_types

from .helpers import handle_sub_plugin_upload


__all__ = (
    'OldSubPluginRelease',
    'SubPlugin',
)


# Create your models here.
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

    allowed_file_types = dict(CommonBase.allowed_file_types)
    allowed_file_types.update({
        'addons/source-python/plugins/{self.plugin.basename}/{sub_plugin_path}/{self.basename}/': [
            'py',
        ] + readable_data_file_types,
    })

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
        self.current_zip_file = self.zip_file
        super(SubPlugin, self).save(
            force_insert, force_update, using, update_fields
        )


class OldSubPluginRelease(models.Model):
    version = models.CharField(
        max_length=8,
    )
    zip_file = models.FileField()
    sub_plugin = models.ForeignKey(
        to='sub_plugins.SubPlugin',
        related_name='previous_releases',
    )
