# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from project_manager.common.constants import (
    ALLOWED_FILE_TYPES, IMAGE_URL, LOGO_URL, READABLE_DATA_FILE_TYPES,
    RELEASE_URL,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PACKAGE_ALLOWED_FILE_TYPES',
    'PACKAGE_IMAGE_URL',
    'PACKAGE_LOGO_URL',
    'PACKAGE_PATH',
    'PACKAGE_RELEASE_URL',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# The base path for packages
PACKAGE_PATH = 'addons/source-python/packages/custom/'

# The allowed file types by directory for packages
PACKAGE_ALLOWED_FILE_TYPES = dict(ALLOWED_FILE_TYPES)
PACKAGE_ALLOWED_FILE_TYPES.update({
    # Just the base file if just a module
    PACKAGE_PATH: ['py'],

    # Other files allowed if in a package
    PACKAGE_PATH + '{self.basename}/': ['py'] + READABLE_DATA_FILE_TYPES,
})

PACKAGE_IMAGE_URL = IMAGE_URL + 'packages/'
PACKAGE_LOGO_URL = LOGO_URL + 'packages/'
PACKAGE_RELEASE_URL = RELEASE_URL + 'packages/'
