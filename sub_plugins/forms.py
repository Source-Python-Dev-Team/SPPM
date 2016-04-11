from zipfile import ZipFile

from django import forms
from django.core.exceptions import ValidationError

from .models import SubPlugin


__all__ = (
    'SubPluginCreateForm',
    'SubPluginUpdateForm',
)


_path = 'addons/source-python/plugins/'


class SubPluginCreateForm(forms.ModelForm):
    class Meta:
        model = SubPlugin
        fields = (
            'name',
            'version',
            'plugin',
            'slug',
            'zip_file',
        )
        widgets = {
            'plugin': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
        }

    def clean_zip_file(self):
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']) if not x.endswith('/')]
        plugin = self.cleaned_data['plugin']
        basename, path = _get_basename(file_list, plugin)
        if not _path + '{0}/{1}/{2}/{2}.py'.format(
                plugin.basename, path, basename) in file_list:
            raise ValidationError(
                'No primary file found in zip.  ' +
                'Perhaps you are attempting to upload a sub-plugin.')
        self.instance.basename = basename
        return self.cleaned_data['zip_file']


class SubPluginUpdateForm(forms.ModelForm):
    class Meta:
        model = SubPlugin
        fields = (
            'version',
            'zip_file',
        )

    def clean_version(self):
        all_versions = [
            x[0] for x in self.instance.previous_releases.values_list(
                'version')] + [self.instance.version]
        if self.cleaned_data['version'] in all_versions:
            raise ValidationError(
                'Release version "{0}" already exists.'.format(
                    self.cleaned_data['version']))
        return self.cleaned_data['version']

    def clean_zip_file(self):
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']).namelist() if not x.endswith('/')]
        plugin = self.instance.plugin
        basename, path = _get_basename(file_list, plugin)
        if not _path + '{0}/{1}/{2}/{2}.py'.format(
                plugin.basename, path, basename) in file_list:
            raise ValidationError(
                'No primary file found in zip.  ' +
                'Perhaps you are attempting to upload a sub-plugin.')
        if basename != plugin.basename:
            raise ValidationError(
                'Uploaded plugin does not match current plugin.')
        return self.cleaned_data['zip_file']


def _get_basename(file_list, plugin):
    plugin_name = _validate_plugin_name(file_list, plugin)
    basename = None
    path = None
    paths = [x[0] for x in plugin.paths.values_list('path')]
    for x in file_list:
        if not x.endswith('.py'):
            continue
        if not x.startswith(_path + '{0}/'.format(plugin_name)):
            continue
        current = x.split(_path + '{0}/'.format(plugin_name), 1)[1]
        if not current:
            continue
        for current_path in paths:
            if not current.startswith(current_path):
                continue
            current = current.split(current_path, 1)[1]
            if current.startswith('/'):
                current = current[1:]
            current = current.split('/', 1)[0]
            if not current:
                continue
            if basename is None:
                basename = current
                path = current_path
            elif basename != current:
                raise ValidationError('Multiple sub-plugins found in zip.')
    if basename is None:
        raise ValidationError('No sub-plugin base directory found in zip.')
    return basename, path


def _validate_plugin_name(file_list, plugin):
    plugin_name = None
    for x in file_list:
        if not x.endswith('.py'):
            continue
        if not x.startswith(_path):
            continue
        current = x.split(_path, 1)[1]
        if not current:
            continue
        current = current.split('/', 1)[0]
        if plugin_name is None:
            plugin_name = current
        elif plugin_name != current:
            raise ValidationError('Multiple plugins found in zip.')
    if plugin_name is None:
        raise ValidationError('No plugin base directory found in zip.')
    if plugin_name != plugin.basename:
        raise ValidationError('Wrong plugin base directory found in zip.')
    return plugin_name
