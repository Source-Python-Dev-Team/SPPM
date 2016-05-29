# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.validators import RegexValidator


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'basename_validator',
    'version_validator',
    'sub_plugin_path_validator',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# basename values should:
#   Start with a lower-case character.
#   Contain only lower-case characters, numbers, and underscores.
#   End in a lower-case character or number.
basename_validator = RegexValidator(r'^[a-z][0-9a-z_]*[0-9a-z]')

# version values should:
#   Start with a number.
#   Contain only numbers, lower-case characters, and decimals.
#   End in a number or lower-case character.
version_validator = RegexValidator(r'^[0-9][0-9a-z.]*[0-9a-z]')

# Sub-plugin paths should:
#   Start with a lower-case character.
#   Contain lower-case characters, numbers, underscores, and (back)slashes
#   End in a lower-case character or number.
sub_plugin_path_validator = RegexValidator(r'^[a-z][0-9a-z/\\_]*[0-9a-z]')
