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
from .helpers import get_sub_plugin_basename
from .models import SubPlugin, SubPluginRelease
from ..plugins.constants import PLUGIN_PATH
from ..users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAddContributorConfirmationForm',
    'SubPluginCreateForm',
    'SubPluginEditForm',
    'SubPluginSelectGamesForm',
    'SubPluginUpdateForm',
)


# =============================================================================
# >> FORM CLASSES
# =============================================================================
class SubPluginCreateForm(forms.ModelForm):
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
        model = SubPlugin
        fields = (
            'name',
            'synopsis',
            'description',
            'configuration',
            'logo',
            'plugin',
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
            'plugin': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(SubPluginCreateForm, self).__init__(*args, **kwargs)
        old_fields = self.fields
        self.fields = OrderedDict([x, old_fields.pop(x)] for x in [
            'name', 'version', 'version_notes', 'zip_file', 'synopsis',
            'description', 'configuration', 'logo',
        ])
        self.fields.update(old_fields)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(SubPluginCreateForm, self).save(commit)
        SubPluginRelease.objects.create(
            sub_plugin=instance,
            version=self.cleaned_data['version'],
            notes=self.cleaned_data['version_notes'],
            zip_file=self.cleaned_data['zip_file'],
        )
        return instance

    def clean_zip_file(self):
        """Verify the zip file contents."""
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']).namelist() if not x.endswith('/')]
        plugin = self.initial['plugin']
        basename, path = get_sub_plugin_basename(file_list, plugin)
        if not (
                '{plugin_path}{plugin_basename}/{path}/{basename}/'
                '{basename}.py'.format(
                    plugin_path=PLUGIN_PATH,
                    plugin_basename=plugin.basename,
                    path=path,
                    basename=basename
                ) in file_list
        ):
            raise ValidationError(
                'No primary file found in zip.  ' +
                'Perhaps you are attempting to upload a sub-plugin.',
                code='not-found',
            )
        current = SubPlugin.objects.filter(plugin=plugin, basename=basename)
        if current:
            raise ValidationError(
                'Sub-plugin {basename} has already been uploaded for '
                'plugin {plugin_name}.'.format(
                    basename=basename,
                    plugin_name=plugin.name
                ),
                code='duplicate',
            )
        self.instance.basename = basename
        return self.cleaned_data['zip_file']


class SubPluginEditForm(forms.ModelForm):
    class Meta:
        model = SubPlugin
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
        super(SubPluginEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class SubPluginSelectGamesForm(forms.ModelForm):
    class Meta:
        model = SubPlugin
        fields = (
            'supported_games',
        )
        widgets = {
            'supported_games': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(SubPluginSelectGamesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


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
        model = SubPluginRelease
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
        super(SubPluginUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(SubPluginUpdateForm, self).save(commit)
        SubPluginRelease.objects.create(
            sub_plugin=instance,
            version=self.cleaned_data['version'],
            notes=self.cleaned_data['notes'],
            zip_file=self.cleaned_data['zip_file'],
        )
        return instance

    def clean_version(self):
        """Verify the version doesn't already exist."""
        all_versions = SubPluginRelease.objects.filter(
            sub_plugin=self.instance
        ).values_list('version', flat=True)
        if self.cleaned_data['version'] in all_versions:
            raise ValidationError(
                'Release version "{version}" already exists.'.format(
                    version=self.cleaned_data['version']
                ),
                code='duplicate'
            )
        return self.cleaned_data['version']

    def clean_zip_file(self):
        """Verify the zip file contents."""
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']).namelist() if not x.endswith('/')]
        plugin = self.instance.plugin
        basename, path = get_sub_plugin_basename(file_list, plugin)
        if not (
                '{plugin_path}{plugin_basename}/{path}/{basename}/'
                '{basename}.py'.format(
                    plugin_path=PLUGIN_PATH,
                    plugin_basename=plugin.basename,
                    path=path,
                    basename=basename
                ) in file_list
        ):
            raise ValidationError(
                'No primary file found in zip.  ' +
                'Perhaps you are attempting to upload a sub-plugin.',
                code='not-found',
            )
        if basename != self.instance.basename:
            raise ValidationError(
                'Uploaded sub-plugin does not match current sub-plugin.',
                code='mismatch',
            )
        return self.cleaned_data['zip_file']
