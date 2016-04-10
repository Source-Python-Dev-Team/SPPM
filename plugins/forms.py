from zipfile import ZipFile

from django import forms
from django.core.exceptions import ValidationError

from .models import Plugin


__all__ = (
    'PluginCreateForm',
    'PluginUpdateForm',
)


class PluginCreateForm(forms.ModelForm):
    class Meta:
        model = Plugin
        fields = (
            'name',
            'version',
            'slug',
            'zip_file',
        )
        widgets = {
            'slug': forms.HiddenInput(),
        }

    def clean_zip_file(self):
        zip_file = ZipFile(self.cleaned_data['zip_file'])
        basename = _get_basename(zip_file)
        self.instance.basename = basename
        return self.cleaned_data['zip_file']


class PluginUpdateForm(forms.ModelForm):
    class Meta:
        model = Plugin
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
        zip_file = ZipFile(self.cleaned_data['zip_file'])
        basename = _get_basename(zip_file)
        if not 'addons/source-python/plugins/{0}/{0}.py'.format(
                basename) in zip_file.namelist():
            raise ValidationError(
                'No primary file found in zip.  ' +
                'Perhaps you are attempting to upload a sub-plugin.')
        if basename != self.instance.basename:
            raise ValidationError(
                'Uploaded plugin does not match current plugin.')
        return self.cleaned_data['zip_file']


def _get_basename(zip_file):
    basename = None
    for x in zip_file.namelist():
        if x.startswith('addons/source-python/plugins/'):
            current = x.split('addons/source-python/plugins/', 1)[1]
            if not current:
                continue
            current = current.split('/', 1)[0]
            if basename is None:
                basename = current
            elif basename != current:
                raise ValidationError(
                    'Multiple base directories found for plugin')
    if basename is None:
        raise ValidationError('No base directory found for plugin.')
    return basename
