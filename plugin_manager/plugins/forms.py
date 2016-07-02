# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from zipfile import ZipFile

# Django
from django import forms
from django.core.exceptions import ValidationError

# 3rd-Party Django
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# App
from .constants import PLUGIN_PATH
from .helpers import get_plugin_basename
from .models import Plugin
from ..users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginAddContributorConfirmationForm',
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

    def __init__(self, *args, **kwargs):
        super(PluginCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_zip_file(self):
        """Verify the zip file contents."""
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']).namelist() if not x.endswith('/')]
        basename = get_plugin_basename(file_list)
        current = Plugin.objects.filter(basename=basename)
        if current:
            raise ValidationError(
                'Plugin {basename} already registered.'.format(
                    basename=basename
                )
            )
        self.instance.basename = basename
        return self.cleaned_data['zip_file']


class PluginEditForm(forms.ModelForm):
    class Meta:
        model = Plugin
        fields = (
            'synopsis',
            'description',
            'configuration',
            'logo',
        )
        widgets = {
            'description': forms.Textarea,
            'configuration': forms.Textarea,
        }

    def __init__(self, *args, **kwargs):
        super(PluginEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class PluginAddContributorConfirmationForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super(PluginUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_version(self):
        """Verify the version doesn't already exist."""
        all_versions = [
            x[0] for x in self.instance.previous_releases.values_list(
                'version')] + [self.instance.version]
        if self.cleaned_data['version'] in all_versions:
            raise ValidationError(
                'Release version "{version}" already exists.'.format(
                    version=self.cleaned_data['version']
                )
            )
        return self.cleaned_data['version']

    def clean_zip_file(self):
        """Verify the zip file contents."""
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']).namelist() if not x.endswith('/')]
        basename = get_plugin_basename(file_list)
        if not '{plugin_path}{basename}/{basename}.py'.format(
            plugin_path=PLUGIN_PATH,
            basename=basename,
        ) in file_list:
            raise ValidationError(
                'No primary file found in zip.  ' +
                'Perhaps you are attempting to upload a sub-plugin.')
        if basename != self.instance.basename:
            raise ValidationError(
                'Uploaded plugin does not match current plugin.')
        return self.cleaned_data['zip_file']
