# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ALLOWED_FILE_TYPES',
    'CANNOT_BE_NAMED',
    'CANNOT_START_WITH',
    'FORUM_THREAD_URL',
    'IMAGE_MAX_HEIGHT',
    'IMAGE_MAX_WIDTH',
    'LOGO_MAX_HEIGHT',
    'LOGO_MAX_WIDTH',
    'MAX_IMAGES',
    'READABLE_DATA_FILE_TYPES',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Base URL for project thread
FORUM_THREAD_URL = settings.FORUM_URL + 'viewtopic.php?t={topic}'

# Maximum allowed width and height for all logo files
LOGO_MAX_WIDTH = 200
LOGO_MAX_HEIGHT = 200

# Maximum allowed width and height for all images (not logos)
IMAGE_MAX_WIDTH = 400
IMAGE_MAX_HEIGHT = 400

# Maximum numbe of images allowed per package, plugin, or sub-plugin
MAX_IMAGES = 10

# URLs
IMAGE_URL = 'images/'
LOGO_URL = 'logos/'
RELEASE_URL = 'releases/'

# Values that packages, plugins, and sub-plugins cannot be named
# Current values are due to the url setup for creating, editing, and updating
CANNOT_BE_NAMED = (
    'create',
)

# Values that packages, plugins, and sub-plugins cannot start with
# Current value is so the package, plugin,
#   or sub-plugin does not seem "official"
CANNOT_START_WITH = (
    'sp_',
)

# Allowed readable file types
READABLE_DATA_FILE_TYPES = [
    'json',
    'ini',
    'res',
    'txt',
    'vdf',
    'xml',
]

# Allowed file types by directory
ALLOWED_FILE_TYPES = {
    'cfg/source-python/': [
        'cfg',
        'ini',
        'md',
    ],

    'log/source-python/': [
        'md',
        'txt',
    ],

    'models/': [
        'ani',
        'mdl',
        'phy',
        'vmf',
        'vmx',
        'vtf',
        'vtx',
        'vvd',
    ],

    'particles/': [
        'pcf',
        'txt',
    ],

    'resource/source-python/events/': [
        'md',
        'res',
        'txt',
    ],

    'resource/source-python/translations/': [
        'md',
        'ini',
    ],

    'sound/source-python/': [
        'mp3',
        'ogg',
        'wav',
    ],
}
