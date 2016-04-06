from django import forms

from .models import SubPlugin


__all__ = (
    'SubPluginCreateForm',
)


class SubPluginCreateForm(forms.ModelForm):
    class Meta:
        model = SubPlugin
        fields = (
            'name',
            'version',
            'plugin',
            'slug',
            'zip_file',
        )
        widgets = {
            'plugin': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
        }
