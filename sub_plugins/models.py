from __future__ import unicode_literals

from django.db import models

from common.models import CommonBase, readable_data_file_types


__all__ = (
    'SubPlugin',
)


# Create your models here.
class SubPlugin(CommonBase):
    """"""

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

    allowed_file_types = dict(CommonBase.allowed_file_types)
    allowed_file_types.update({
        'addons/source-python/plugins/{self.plugin.basename}/{sub_plugin_path}/{self.basename}/': [
            'py',
        ] + readable_data_file_types,
    })

    def get_basename(self, zip_file):
        plugin_name = self.validate_plugin_name(zip_file)
        basename = None
        for x in zip_file.filelist:
            if not x.filename.startswith(
                    'addons/source-python/plugins/{0}/'.format(plugin_name)):
                continue
            current = x.filename.split(
                'addons/source-python/plugins/{0}/'.format(plugin_name), 1)[1]
            if not current:
                continue
            for path in self.plugin.paths.all():
                if not current.startswith(path.path):
                    continue
                current = current.split(path.path, 1)[1]
                if current.startswith('/'):
                    current = current[1:]
                current = current.split('/', 1)[0]
                if not current:
                    continue
                if basename is None:
                    basename = current
                elif basename != current:
                    raise ValueError('Multiple sub-plugins found in zip.')
        if basename is None:
            raise ValueError('No sub-plugin base directory found in zip.')
        return basename

    def validate_plugin_name(self, zip_file):
        plugin_name = None
        for x in zip_file.filelist:
            if not x.filename.startswith('addons/source-python/plugins/'):
                continue
            current = x.filename.split(
                'addons/source-python/plugins/', 1)[1]
            if not current:
                continue
            current = current.split('/', 1)[0]
            if plugin_name is None:
                plugin_name = current
            elif plugin_name != current:
                raise ValueError('Multiple plugins found in zip.')
        if plugin_name is None:
            raise ValueError('No plugin base directory found in zip.')
        if plugin_name != self.plugin.basename:
            raise ValueError('Wrong plugin base directory found in zip.')
        return plugin_name
