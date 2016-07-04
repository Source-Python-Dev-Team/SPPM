# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from plugin_manager.common.constants import (
    ALLOWED_FILE_TYPES, IMAGE_URL, LOGO_URL, READABLE_DATA_FILE_TYPES,
    RELEASE_URL,
)
from plugin_manager.plugins.constants import PLUGIN_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SUB_PLUGIN_ALLOWED_FILE_TYPES',
    'SUB_PLUGIN_IMAGE_URL',
    'SUB_PLUGIN_LOGO_URL',
    'SUB_PLUGIN_RELEASE_URL',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# The allowed file types by directory for sub-plugins
SUB_PLUGIN_ALLOWED_FILE_TYPES = dict(ALLOWED_FILE_TYPES)
SUB_PLUGIN_ALLOWED_FILE_TYPES.update({
    PLUGIN_PATH + '{self.plugin.basename}/{sub_plugin_path}/'
    '{self.basename}/': ['py'] + READABLE_DATA_FILE_TYPES,
})

SUB_PLUGIN_IMAGE_URL = IMAGE_URL + 'sub-plugins/'
SUB_PLUGIN_LOGO_URL = LOGO_URL + 'sub-plugins/'
SUB_PLUGIN_RELEASE_URL = RELEASE_URL + 'sub-plugins/'
