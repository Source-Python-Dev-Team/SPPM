# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ALLOWED_FILE_TYPES',
    'CANNOT_BE_NAMED',
    'CANNOT_START_WITH',
    'LOGO_MAX_HEIGHT',
    'LOGO_MAX_WIDTH',
    'IMAGE_MAX_HEIGHT',
    'IMAGE_MAX_WIDTH',
    'MAX_IMAGES',
    'READABLE_DATA_FILE_TYPES',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
LOGO_MAX_WIDTH = 200
LOGO_MAX_HEIGHT = 200

IMAGE_MAX_WIDTH = 400
IMAGE_MAX_HEIGHT = 400

MAX_IMAGES = 10

CANNOT_BE_NAMED = (
    'create',
    'edit',
    'update',
)

CANNOT_START_WITH = (
    'sp_',
)

READABLE_DATA_FILE_TYPES = [
    'json',
    'ini',
    'res',
    'txt',
    'vdf',
    'xml',
]

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
