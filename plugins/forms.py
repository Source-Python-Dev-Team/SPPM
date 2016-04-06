from common.forms import BaseCreateForm

from .models import Plugin


__all__ = (
    'PluginCreateForm',
)


class PluginCreateForm(BaseCreateForm):
    class Meta(BaseCreateForm.Meta):
        model = Plugin
