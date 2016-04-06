from django import forms

from plugins.models import Plugin

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
            'zip_file',
        )

    def __init__(self, *args, **kwargs):
        plugin = Plugin.objects.get(basename=kwargs.pop('plugin_name'))
        super(SubPluginCreateForm, self).__init__(*args, **kwargs)
        self.instance.plugin = plugin
