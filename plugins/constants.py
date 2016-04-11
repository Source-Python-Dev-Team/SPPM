from common.constants import ALLOWED_FILE_TYPES, READABLE_DATA_FILE_TYPES

PLUGIN_ALLOWED_FILE_TYPES = dict(ALLOWED_FILE_TYPES)
PLUGIN_ALLOWED_FILE_TYPES.update({
    'addons/source-python/plugins/{self.basename}/': [
        'py',
    ] + READABLE_DATA_FILE_TYPES,
})
