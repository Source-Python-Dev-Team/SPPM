from common.constants import ALLOWED_FILE_TYPES, READABLE_DATA_FILE_TYPES


__all__ = (
    'PACKAGE_ALLOWED_FILE_TYPES',
    'PACKAGE_PATH',
)


PACKAGE_PATH = 'addons/source-python/packages/custom/'

PACKAGE_ALLOWED_FILE_TYPES = dict(ALLOWED_FILE_TYPES)
PACKAGE_ALLOWED_FILE_TYPES.update({
    'addons/source-python/packages/custom/': [
        'py',
    ] + READABLE_DATA_FILE_TYPES,
})
