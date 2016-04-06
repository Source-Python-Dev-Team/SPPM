from django import forms

from .models import Plugin


__all__ = (
    'PluginCreateForm',
)


class PluginCreateForm(forms.ModelForm):
    class Meta:
        model = Plugin
        fields = (
            'name',
            'version',
            'zip_file',
        )
