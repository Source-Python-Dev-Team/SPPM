"""SubPluginPath validators."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.validators import RegexValidator


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'sub_plugin_path_validator',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Sub-plugin paths should:
#   Start with a lower-case character.
#   Contain lower-case characters, numbers, underscores, and (back)slashes
#   End in a lower-case character or number.
sub_plugin_path_validator = RegexValidator(r'^[a-z][0-9a-z/\\_]*[0-9a-z]')
