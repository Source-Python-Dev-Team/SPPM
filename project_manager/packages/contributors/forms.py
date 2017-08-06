"""Package contributors forms."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django import forms

# App
from project_manager.users.models import ForumUser


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
    """Form for confirming adding a contributor to a Package."""

    class Meta:
        model = ForumUser
        fields = (
            "id",
        )
        widgets = {
            "id": forms.HiddenInput(),
        }

    def validate_unique(self):
        """Override validate_unique to do nothing."""
        pass
