from __future__ import unicode_literals

from django.db import models

from common.models import CommonBase, readable_data_file_types
from common.validators import sub_plugin_path_validator

from .helpers import handle_plugin_upload


__all__ = (
    'Plugin',
    'SubPluginPath',
)


# Create your models here.
class Plugin(CommonBase):
    """"""

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

    allowed_file_types = dict(CommonBase.allowed_file_types)
    allowed_file_types.update({
        'addons/source-python/plugins/{self.basename}/': [
                                                             'py',
                                                         ] + readable_data_file_types,
    })

    def get_basename(self, zip_file):
        basename = None
        for x in zip_file.filelist:
            if x.filename.startswith('addons/source-python/plugins/'):
                current = x.filename.split(
                    'addons/source-python/plugins/', 1)[1]
                if not current:
                    continue
                current = current.split('/', 1)[0]
                if basename is None:
                    basename = current
                elif basename != current:
                    raise ValueError
        if basename is None:
            raise ValueError
        return basename


class SubPluginPath(models.Model):

    plugin = models.ForeignKey(
        to='plugins.Plugin',
        related_name='paths',
    )

    path = models.CharField(
        max_length=256,
        validators=[sub_plugin_path_validator],
    )
