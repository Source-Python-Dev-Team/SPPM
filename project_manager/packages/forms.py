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
from .constants import PACKAGE_PATH
from .helpers import get_package_basename
from .models import Package, PackageRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageCreateForm',
    'PackageEditForm',
    'PackageSelectGamesForm',
    'PackageUpdateForm',
)


# =============================================================================
# >> FORMS
# =============================================================================
class PackageCreateForm(SubmitButtonMixin):
    version = forms.CharField(
        max_length=8,
        help_text=PackageRelease._meta.get_field('version').help_text,
    )
    version_notes = forms.CharField(
        max_length=512,
        required=False,
        help_text=PackageRelease._meta.get_field('notes').help_text,
        widget=forms.Textarea(
            attrs={
                'cols': '64',
                'rows': '8',
            }
        )
    )
    zip_file = forms.FileField(
        help_text=PackageRelease._meta.get_field('zip_file').help_text,
    )

    class Meta:
        model = Package
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
        super(PackageCreateForm, self).__init__(*args, **kwargs)
        old_fields = self.fields
        self.fields = OrderedDict([x, old_fields.pop(x)] for x in [
            'name', 'version', 'version_notes', 'zip_file', 'synopsis',
            'description', 'configuration', 'logo',
        ])
        self.fields.update(old_fields)

    def save(self, commit=True):
        instance = super(PackageCreateForm, self).save(commit)
        PackageRelease.objects.create(
            package=instance,
            version=self.cleaned_data['version'],
            notes=self.cleaned_data['version_notes'],
            zip_file=self.cleaned_data['zip_file'],
        )
        return instance

    def clean_zip_file(self):
        """Verify the zip file contents."""
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']).namelist() if not x.endswith('/')]
        basename = get_package_basename(file_list)
        current = Package.objects.filter(basename=basename)
        if current:
            raise ValidationError(
                f'Package {basename} is already registered.',
                code='duplicate',
            )
        self.instance.basename = basename
        return self.cleaned_data['zip_file']


class PackageEditForm(SubmitButtonMixin):
    class Meta:
        model = Package
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


class PackageSelectGamesForm(SubmitButtonMixin):
    class Meta:
        model = Package
        fields = (
            'supported_games',
        )
        widgets = {
            'supported_games': forms.CheckboxSelectMultiple()
        }


class PackageUpdateForm(SubmitButtonMixin):
    class Meta:
        model = PackageRelease
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
        instance = super(PackageUpdateForm, self).save(commit)
        PackageRelease.objects.create(
            package=instance,
            version=self.cleaned_data['version'],
            notes=self.cleaned_data['notes'],
            zip_file=self.cleaned_data['zip_file'],
        )
        return instance

    def clean_version(self):
        """Verify the version doesn't already exist."""
        all_versions = PackageRelease.objects.filter(
            package=self.instance
        ).values_list('version', flat=True)
        version = self.cleaned_data['version']
        if version in all_versions:
            raise ValidationError(
                f'Release version "{version}" already exists.',
                code='duplicate',
            )
        return version

    def clean_zip_file(self):
        """Verify the zip file contents."""
        file_list = [x for x in ZipFile(
            self.cleaned_data['zip_file']).namelist() if not x.endswith('/')]
        basename, is_module = get_package_basename(file_list)
        if (
            not is_module and
            f'{PACKAGE_PATH}{basename}/{basename}.py' in file_list
        ):
            raise ValidationError(
                'No primary file found in zip.',
                code='not-found',
            )
        if basename != self.instance.basename:
            raise ValidationError(
                'Uploaded package does not match current package.',
                code='mismatch',
            )
        return self.cleaned_data['zip_file']
