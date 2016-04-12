# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ALLOWED_FILE_TYPES',
    'READABLE_DATA_FILE_TYPES',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
LOGO_MAX_WIDTH = 200
LOGO_MAX_HEIGHT = 200

IMAGE_MAX_WIDTH = 400
IMAGE_MAX_HEIGHT = 400

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
