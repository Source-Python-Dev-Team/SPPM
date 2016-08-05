# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# App
from .constants import (
    PLUGIN_PATH, PLUGIN_IMAGE_URL, PLUGIN_LOGO_URL, PLUGIN_RELEASE_URL,
)
from project_manager.common.constants import CANNOT_BE_NAMED, CANNOT_START_WITH
from project_manager.common.helpers import find_image_number


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
                'Multiple base directories found for plugin',
                code='multiple',
            )
    if basename is None:
        raise ValidationError(
            'No base directory found for plugin.',
            code='not-found',
        )
    if basename in CANNOT_BE_NAMED:
        raise ValidationError(
            'Plugin basename cannot be "{basename}".'.format(
                basename=basename
            ),
            code='invalid',
        )
    for start in CANNOT_START_WITH:
        if basename.startswith(start):
            raise ValidationError(
                'Plugin basename cannot start with "{start}".'.format(
                    start=start,
                ),
                code='invalid',
            )
    return basename


def handle_plugin_zip_upload(instance, filename):
    """Return the path to store the zip for the current release."""
    return '{release_url}{slug}/{slug}-v{version}.zip'.format(
        release_url=PLUGIN_RELEASE_URL,
        slug=instance.plugin.slug,
        version=instance.version,
    )


def handle_plugin_logo_upload(instance, filename):
    """Return the path to store the plugin's logo."""
    return '{logo_url}{slug}.{extension}'.format(
        logo_url=PLUGIN_LOGO_URL,
        slug=instance.slug,
        extension=filename.rsplit('.', 1)[1],
    )


def handle_plugin_image_upload(instance, filename):
    """Return the path to store the image."""
    return '{image_url}{slug}/{image_number}.{extension}'.format(
        image_url=PLUGIN_IMAGE_URL,
        slug=instance.plugin.slug,
        image_number=find_image_number('plugin', instance.plugin.slug),
        extension=filename.rsplit('.', 1)[1],
    )
