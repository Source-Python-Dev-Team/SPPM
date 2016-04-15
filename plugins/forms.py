# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from zipfile import ZipFile

# Django Imports
from django import forms
from django.core.exceptions import ValidationError

# App Imports
from .constants import PLUGIN_PATH
from .helpers import get_plugin_basename
from .models import Plugin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginCreateForm',
    'PluginEditForm',
    'PluginUpdateForm',
)


# =============================================================================
# >> FORM CLASSES
# =============================================================================
class PluginCreateForm(forms.ModelForm):
    class Meta:
        model = Plugin
        fields = (
            'name',
            'version',
            'description',
            'version_notes',
            'configuration',
            'logo',
            'slug',
            'zip_file',
        )
        widgets = {
            'slug': forms.HiddenInput(),
            'description': forms.Textarea,
            'version_notes': forms.Textarea,
            'configuration': forms.Textarea,
        }

    def clean_zip_file(self):
        """Verify the zip file contents."""
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']) if not x.endswith('/')]
        basename = get_plugin_basename(file_list)
        self.instance.basename = basename
        return self.cleaned_data['zip_file']


class PluginEditForm(forms.ModelForm):
    class Meta:
        model = Plugin
        fields = (
            'description',
            'configuration',
            'logo',
        )
        widgets = {
            'description': forms.Textarea,
            'configuration': forms.Textarea,
        }


class PluginUpdateForm(forms.ModelForm):
    class Meta:
        model = Plugin
        fields = (
            'version',
            'version_notes',
            'zip_file',
        )
        widgets = {
            'version_notes': forms.Textarea,
        }

    def clean_version(self):
        """Verify the version doesn't already exist."""
        all_versions = [
            x[0] for x in self.instance.previous_releases.values_list(
                'version')] + [self.instance.version]
        if self.cleaned_data['version'] in all_versions:
            raise ValidationError(
                'Release version "{0}" already exists.'.format(
                    self.cleaned_data['version']))
        return self.cleaned_data['version']

    def clean_zip_file(self):
        """Verify the zip file contents."""
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']).namelist() if not x.endswith('/')]
        basename = get_plugin_basename(file_list)
        if not PLUGIN_PATH + '{0}/{0}.py'.format(basename) in file_list:
            raise ValidationError(
                'No primary file found in zip.  ' +
                'Perhaps you are attempting to upload a sub-plugin.')
        if basename != self.instance.basename:
            raise ValidationError(
                'Uploaded plugin does not match current plugin.')
        return self.cleaned_data['zip_file']
