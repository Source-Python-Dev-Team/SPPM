# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import OrderedDict
from zipfile import ZipFile

# Django
from django import forms
from django.core.exceptions import ValidationError

# App
from project_manager.common.mixins import SubmitButtonMixin
from .helpers import get_sub_plugin_basename
from .models import SubPlugin, SubPluginRelease
from project_manager.plugins.constants import PLUGIN_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginCreateForm',
    'SubPluginEditForm',
    'SubPluginSelectGamesForm',
    'SubPluginUpdateForm',
)


# =============================================================================
# >> FORMS
# =============================================================================
class SubPluginCreateForm(SubmitButtonMixin):
    version = forms.CharField(
        max_length=8,
        help_text=SubPluginRelease._meta.get_field('version').help_text,
    )
    version_notes = forms.CharField(
        max_length=512,
        required=False,
        help_text=SubPluginRelease._meta.get_field('notes').help_text,
        widget=forms.Textarea(
            attrs={
                'cols': '64',
                'rows': '8',
            }
        )
    )
    zip_file = forms.FileField(
        help_text=SubPluginRelease._meta.get_field('zip_file').help_text,
    )

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
        self.cleaned_data['path'] = path
        return self.cleaned_data['zip_file']


class SubPluginEditForm(SubmitButtonMixin):
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


class SubPluginSelectGamesForm(SubmitButtonMixin):
    class Meta:
        model = SubPlugin
        fields = (
            'supported_games',
        )
        widgets = {
            'supported_games': forms.CheckboxSelectMultiple()
        }


class SubPluginUpdateForm(SubmitButtonMixin):
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
        self.cleaned_data['path'] = path
        return self.cleaned_data['zip_file']
