# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from ..common.constants import ALLOWED_FILE_TYPES, READABLE_DATA_FILE_TYPES
from ..plugins.constants import PLUGIN_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SUB_PLUGIN_ALLOWED_FILE_TYPES',
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
