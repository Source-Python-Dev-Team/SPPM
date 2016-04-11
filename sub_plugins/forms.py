from zipfile import ZipFile

from django import forms
from django.core.exceptions import ValidationError

from plugins.constants import PLUGIN_PATH

from .helpers import get_sub_plugin_basename
from .models import SubPlugin


__all__ = (
    'SubPluginCreateForm',
    'SubPluginEditForm',
    'SubPluginUpdateForm',
)


class SubPluginCreateForm(forms.ModelForm):
    class Meta:
        model = SubPlugin
        fields = (
            'name',
            'version',
            'description',
            'version_notes',
            'configuration',
            'plugin',
            'slug',
            'zip_file',
        )
        widgets = {
            'plugin': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
            'description': forms.Textarea,
            'version_notes': forms.Textarea,
            'configuration': forms.Textarea,
        }

    def clean_zip_file(self):
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']) if not x.endswith('/')]
        plugin = self.cleaned_data['plugin']
        basename, path = get_sub_plugin_basename(file_list, plugin)
        if not PLUGIN_PATH + '{0}/{1}/{2}/{2}.py'.format(
                plugin.basename, path, basename) in file_list:
            raise ValidationError(
                'No primary file found in zip.  ' +
                'Perhaps you are attempting to upload a sub-plugin.')
        self.instance.basename = basename
        return self.cleaned_data['zip_file']


class SubPluginEditForm(forms.ModelForm):
    class Meta:
        model = SubPlugin
        fields = (
            'description',
            'configuration',
        )
        widgets = {
            'description': forms.Textarea,
            'configuration': forms.Textarea,
        }


class SubPluginUpdateForm(forms.ModelForm):
    class Meta:
        model = SubPlugin
        fields = (
            'version',
            'version_notes',
            'zip_file',
        )
        widgets = {
            'version_notes': forms.Textarea,
        }

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
        basename, path = get_sub_plugin_basename(file_list, plugin)
        if not PLUGIN_PATH + '{0}/{1}/{2}/{2}.py'.format(
                plugin.basename, path, basename) in file_list:
            raise ValidationError(
                'No primary file found in zip.  ' +
                'Perhaps you are attempting to upload a sub-plugin.')
        if basename != plugin.basename:
            raise ValidationError(
                'Uploaded plugin does not match current plugin.')
        return self.cleaned_data['zip_file']
