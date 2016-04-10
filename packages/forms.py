from django import forms
from django.core.exceptions import ValidationError

from .models import Package


__all__ = (
    'PackageCreateForm',
    'PackageUpdateForm',
)


class PackageCreateForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = (
            'name',
            'version',
            'slug',
            'zip_file',
        )
        widgets = {
            'slug': forms.HiddenInput(),
        }


class PackageUpdateForm(forms.ModelForm):
    class Meta:
        model = Package
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
