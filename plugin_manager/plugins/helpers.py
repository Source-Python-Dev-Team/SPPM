# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# App
from .constants import PLUGIN_PATH
from ..common.constants import CANNOT_BE_NAMED, CANNOT_START_WITH
from ..common.helpers import find_image_number


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'get_plugin_basename',
    'handle_plugin_image_upload',
    'handle_plugin_logo_upload',
    'handle_plugin_zip_upload',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_plugin_basename(file_list):
    """Return the plugin's basename."""
    basename = None
    for file_path in file_list:
        if not file_path.endswith('.py'):
            continue
        if not file_path.startswith(PLUGIN_PATH):
            continue
        current = file_path.split(PLUGIN_PATH, 1)[1]
        if not current:
            continue
        current = current.split('/', 1)[0]
        if basename is None:
            basename = current
        elif basename != current:
            raise ValidationError(
                'Multiple base directories found for plugin')
    if basename is None:
        raise ValidationError('No base directory found for plugin.')
    if basename in CANNOT_BE_NAMED:
        raise ValidationError(
            'Plugin basename cannot be "{basename}".'.format(
                basename=basename
            )
        )
    if basename.startswith(CANNOT_START_WITH):
        raise ValidationError(
            'Plugin basename cannot start with "{basename}".'.format(
                basename=basename
            )
        )
    return basename


def handle_plugin_zip_upload(instance, filename):
    """Return the path to store the zip for the current release."""
    return 'releases/plugins/{basename}/{basename}-v{version}.zip'.format(
        basename=instance.basename,
        version=instance.version,
    )


def handle_plugin_logo_upload(instance, filename):
    """Return the path to store the plugin's logo."""
    return 'logos/plugins/{basename}.{extension}'.format(
        basename=instance.basename,
        extension=filename.rsplit('.', 1)[1],
    )


def handle_plugin_image_upload(instance, filename):
    """Return the path to store the image."""
    return 'images/plugins/{basename}/{image_number}.{extension}'.format(
        basename=instance.plugin.basename,
        image_number=find_image_number('plugin', instance.plugin.basename),
        extension=filename.rsplit('.', 1)[1],
    )
