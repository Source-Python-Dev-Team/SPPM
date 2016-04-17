# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from zipfile import ZipFile

# Django Imports
from django import forms
from django.core.exceptions import ValidationError

# Project Imports
from plugins.constants import PLUGIN_PATH
from users.models import ForumUser

# App Imports
from .helpers import get_sub_plugin_basename
from .models import SubPlugin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAddContributorConfirmationForm',
    'SubPluginCreateForm',
    'SubPluginEditForm',
    'SubPluginUpdateForm',
)


# =============================================================================
# >> FORM CLASSES
# =============================================================================
class SubPluginCreateForm(forms.ModelForm):
    class Meta:
        model = SubPlugin
        fields = (
            'name',
            'version',
            'description',
            'version_notes',
            'configuration',
            'logo',
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
        """Verify the zip file contents."""
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']).namelist() if not x.endswith('/')]
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
            'logo',
        )
        widgets = {
            'description': forms.Textarea,
            'configuration': forms.Textarea,
        }


class SubPluginAddContributorConfirmationForm(forms.ModelForm):
    class Meta:
        model = ForumUser
        fields = (
            "id",
        )
        widgets = {
            "id": forms.HiddenInput(),
        }

    def validate_unique(self):
        pass


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
        plugin = self.instance.plugin
        basename, path = get_sub_plugin_basename(file_list, plugin)
        if not PLUGIN_PATH + '{0}/{1}/{2}/{2}.py'.format(
                plugin.basename, path, basename) in file_list:
            raise ValidationError(
                'No primary file found in zip.  ' +
                'Perhaps you are attempting to upload a sub-plugin.')
        if basename != self.instance.basename:
            raise ValidationError(
                'Uploaded plugin does not match current plugin.')
        return self.cleaned_data['zip_file']
