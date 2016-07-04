# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import OrderedDict
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
from .models import Plugin, PluginRelease
from ..users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginAddContributorConfirmationForm',
    'PluginCreateForm',
    'PluginEditForm',
    'PluginSelectGamesForm',
    'PluginUpdateForm',
)


# =============================================================================
# >> FORM CLASSES
# =============================================================================
class PluginCreateForm(forms.ModelForm):
    version = forms.CharField(
        max_length=8,
    )
    version_notes = forms.CharField(
        max_length=512,
        required=False,
        widget=forms.Textarea(
            attrs={
                'cols': '64',
                'rows': '8',
            }
        )
    )
    zip_file = forms.FileField()

    class Meta:
        model = Plugin
        fields = (
            'name',
            'synopsis',
            'description',
            'configuration',
            'logo',
            'slug',
        )
        widgets = {
            'synopsis': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '2',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '16',
                }
            ),
            'configuration': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '16',
                }
            ),
            'slug': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PluginCreateForm, self).__init__(*args, **kwargs)
        old_fields = self.fields
        self.fields = OrderedDict([x, old_fields.pop(x)] for x in [
            'name', 'version', 'version_notes', 'zip_file', 'synopsis',
            'description', 'configuration', 'logo',
        ])
        self.fields.update(old_fields)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(PluginCreateForm, self).save(commit)
        PluginRelease.objects.create(
            plugin=instance,
            version=self.cleaned_data['version'],
            notes=self.cleaned_data['version_notes'],
            zip_file=self.cleaned_data['zip_file'],
        )
        return instance

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
                ),
                code='duplicate',
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
            'synopsis': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '2',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '16',
                }
            ),
            'configuration': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '16',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(PluginEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class PluginSelectGamesForm(forms.ModelForm):
    class Meta:
        model = Plugin
        fields = (
            'supported_games',
        )
        widgets = {
            'supported_games': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(PluginSelectGamesForm, self).__init__(*args, **kwargs)
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
        model = PluginRelease
        fields = (
            'version',
            'notes',
            'zip_file',
        )
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'cols': '64',
                    'rows': '8',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(PluginUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(PluginUpdateForm, self).save(commit)
        PluginRelease.objects.create(
            plugin=instance,
            version=self.cleaned_data['version'],
            notes=self.cleaned_data['notes'],
            zip_file=self.cleaned_data['zip_file'],
        )
        return instance

    def clean_version(self):
        """Verify the version doesn't already exist."""
        all_versions = PluginRelease.objects.filter(
            plugin=self.instance
        ).values_list('version', flat=True)
        if self.cleaned_data['version'] in all_versions:
            raise ValidationError(
                'Release version "{version}" already exists.'.format(
                    version=self.cleaned_data['version']
                ),
                code='duplicate',
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
                'Perhaps you are attempting to upload a sub-plugin.',
                code='not-found',
            )
        if basename != self.instance.basename:
            raise ValidationError(
                'Uploaded plugin does not match current plugin.',
                code='mismatch',
            )
        return self.cleaned_data['zip_file']
