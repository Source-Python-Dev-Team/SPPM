"""Widgets to use for SubPlugin admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib.admin import widgets


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginRawIdWidget',
)


# =============================================================================
# >> WIDGETS
# =============================================================================
class PluginRawIdWidget(widgets.ForeignKeyRawIdWidget):
    """Widget to use for selecting the Plugin for a SubPlugin."""

    def url_parameters(self):
        """Set the parameter to limit Plugins to only those with paths."""
        res = super().url_parameters()
        res['paths__isnull'] = '0'
        return res
