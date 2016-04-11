from zipfile import ZipFile

from django import forms
from django.core.exceptions import ValidationError

from .models import Package


__all__ = (
    'PackageCreateForm',
    'PackageUpdateForm',
)


_path = 'addons/source-python/packages/custom/'


class PackageCreateForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = (
            'name',
            'version',
            'version_notes',
            'slug',
            'zip_file',
        )
        widgets = {
            'slug': forms.HiddenInput(),
            'version_notes': forms.Textarea,
        }

    def clean_zip_file(self):
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']) if not x.endswith('/')]
        basename = _get_basename(file_list)
        self.instance.basename = basename
        return self.cleaned_data['zip_file']


class PackageUpdateForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = (
            'version',
            'version_notes',
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
            self.cleaned_data['zip_file']) if not x.endswith('/')]
        basename, is_module = _get_basename(file_list)
        if not is_module and _path + '{0}/{0}.py'.format(
                basename) in file_list:
            raise ValidationError('No primary file found in zip.')
        if basename != self.instance.basename:
            raise ValidationError(
                'Uploaded plugin does not match current plugin.')
        return self.cleaned_data['zip_file']


def _get_basename(file_list):
    basename = None
    is_module = False
    for x in file_list:
        if not x.endswith('.py'):
            continue
        if not x.startswith(_path):
            continue
        current = x.split(_path, 1)[1]
        if not current:
            continue
        if '/' not in current:
            current = current.rsplit('.', 1)[0]
            is_module = True
        else:
            current = current.split('/', 1)[0]
        if basename is None:
            basename = current
        elif basename != current:
            raise ValidationError('Multiple base directories found for plugin')
    if basename is None:
        raise ValidationError('No base directory found for plugin.')
    return basename, is_module
