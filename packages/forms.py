from django import forms

from .models import Package


__all__ = (
    'PackageCreateForm',
)


class PackageCreateForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = (
            'name',
            'version',
            'zip_file',
        )
