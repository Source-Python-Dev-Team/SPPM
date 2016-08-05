# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django import forms

# 3rd-Party Django
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# App
from .models import SubPluginPath


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginPathCreateForm',
    'SubPluginPathEditForm',
)


# =============================================================================
# >> FORMS
# =============================================================================
class SubPluginPathCreateForm(forms.ModelForm):
    class Meta:
        model = SubPluginPath
        fields = (
            'path',
            'plugin',
        )
        widgets = {
            'plugin': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(SubPluginPathCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class SubPluginPathEditForm(forms.ModelForm):
    class Meta:
        model = SubPluginPath
        fields = (
            'path',
        )

    def __init__(self, *args, **kwargs):
        super(SubPluginPathEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
