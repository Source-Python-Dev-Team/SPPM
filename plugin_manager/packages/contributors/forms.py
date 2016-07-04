# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django import forms

# App
from plugin_manager.users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAddContributorConfirmationForm',
)


# =============================================================================
# >> FORMS
# =============================================================================
class PackageAddContributorConfirmationForm(forms.ModelForm):
    class Meta:
        model = ForumUser
        fields = (
            "id",
        )
        widgets = {
            "id": forms.HiddenInput(),
        }

    def validate_unique(self):
        pass
