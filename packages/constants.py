from common.constants import ALLOWED_FILE_TYPES, READABLE_DATA_FILE_TYPES

PACKAGE_ALLOWED_FILE_TYPES = dict(ALLOWED_FILE_TYPES)
PACKAGE_ALLOWED_FILE_TYPES.update({
    'addons/source-python/packages/custom/': [
        'py',
    ] + READABLE_DATA_FILE_TYPES,
})
