"""Base constants."""

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
    'IMAGE_URL',
    'LOGO_MAX_HEIGHT',
    'LOGO_MAX_WIDTH',
    'LOGO_URL',
    'MAX_IMAGES',
    'PROJECT_BASENAME_MAX_LENGTH',
    'PROJECT_CONFIGURATION_MAX_LENGTH',
    'PROJECT_DESCRIPTION_MAX_LENGTH',
    'PROJECT_NAME_MAX_LENGTH',
    'PROJECT_SLUG_MAX_LENGTH',
    'PROJECT_SYNOPSIS_MAX_LENGTH',
    'READABLE_DATA_FILE_TYPES',
    'RELEASE_NOTES_MAX_LENGTH',
    'RELEASE_REQUIREMENT_ERRORS_MAX_LENGTH',
    'RELEASE_URL',
    'RELEASE_VERSION_MAX_LENGTH',
    'VCS_REQUIREMENT_TYPES',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Max length constants
PROJECT_BASENAME_MAX_LENGTH = 32
PROJECT_CONFIGURATION_MAX_LENGTH = 1024
PROJECT_DESCRIPTION_MAX_LENGTH = 1024
PROJECT_NAME_MAX_LENGTH = 64
PROJECT_SLUG_MAX_LENGTH = 32
PROJECT_SYNOPSIS_MAX_LENGTH = 128
RELEASE_NOTES_MAX_LENGTH = 512
RELEASE_REQUIREMENT_ERRORS_MAX_LENGTH = 1024
RELEASE_VERSION_MAX_LENGTH = 8

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

VCS_REQUIREMENT_TYPES = {
    'git': (
        '<a href="https://git-scm.com/book/en/v2/Getting-Started-'
        'Installing-Git">Git</a>'
    ),
    'hg': (
        '<a href="https://www.mercurial-scm.org/wiki/Download">Mercurial</a>'
    ),
    'svn': (
        '<a href="http://subversion.apache.org/packages.html">SubVersion</a>'
    ),
    'bzr': (
        '<a href="http://doc.bazaar.canonical.com/latest/en/user-guide/'
        'installing_bazaar.html">Bazaar</a>'
    ),
}

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
