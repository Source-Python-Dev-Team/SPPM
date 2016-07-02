# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from ..common.constants import (
    ALLOWED_FILE_TYPES, IMAGE_URL, LOGO_URL, READABLE_DATA_FILE_TYPES,
    RELEASE_URL,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PLUGIN_ALLOWED_FILE_TYPES',
    'PLUGIN_IMAGE_URL',
    'PLUGIN_LOGO_URL',
    'PLUGIN_PATH',
    'PLUGIN_RELEASE_URL',
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

PLUGIN_IMAGE_URL = IMAGE_URL + 'plugins/'
PLUGIN_LOGO_URL = LOGO_URL + 'plugins/'
PLUGIN_RELEASE_URL = RELEASE_URL + 'plugins/'
