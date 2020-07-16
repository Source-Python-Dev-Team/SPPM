"""Forms to use for SubPlugin admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django import forms
from django.contrib.admin.sites import site

# App
from project_manager.sub_plugins.admin.widgets import PluginRawIdWidget
from project_manager.sub_plugins.models import SubPlugin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginAdminForm',
)


# =============================================================================
# >> ADMIN FORMS
# =============================================================================
class SubPluginAdminForm(forms.ModelForm):
    """Form to use for selecting the Plugin for a SubPlugin."""

    def __init__(self, *args, **kwargs):
        """Set the widget."""
        super().__init__(*args, **kwargs)
        self.fields['plugin'].queryset = self.fields['plugin'].queryset.filter(
            paths__isnull=False,
        )
        self.fields['plugin'].widget = PluginRawIdWidget(
            rel=SubPlugin._meta.get_field('plugin').remote_field,
            admin_site=site,
        )
