"""SubPluginPath forms."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django import forms

# App
from project_manager.common.mixins import SubmitButtonMixin
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
class SubPluginPathCreateForm(SubmitButtonMixin):
    """SubPluginPath creation form."""

    class Meta:
        model = SubPluginPath
        fields = (
            'path',
            'plugin',
        )
        widgets = {
            'plugin': forms.HiddenInput(),
        }


class SubPluginPathEditForm(SubmitButtonMixin):
    """SubPluginPath update form."""

    class Meta:
        model = SubPluginPath
        fields = (
            'path',
        )
