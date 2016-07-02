# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from ..common.constants import ALLOWED_FILE_TYPES, READABLE_DATA_FILE_TYPES


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PLUGIN_ALLOWED_FILE_TYPES',
    'PLUGIN_PATH',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# The base path for plugins
PLUGIN_PATH = 'addons/source-python/plugins/'

# The allowed file types by directory for plugins
PLUGIN_ALLOWED_FILE_TYPES = dict(ALLOWED_FILE_TYPES)
PLUGIN_ALLOWED_FILE_TYPES.update({
    PLUGIN_PATH + '{self.basename}/': ['py'] + READABLE_DATA_FILE_TYPES,
})
