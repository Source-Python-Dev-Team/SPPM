# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from zipfile import ZipFile, BadZipfile

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
def get_plugin_basename(zip_file):
    """Return the plugin's basename."""
    try:
        file_list = [
            x for x in ZipFile(zip_file).namelist() if not x.endswith('/')
        ]
    except BadZipfile:
        raise ValidationError({
            'zip_file': 'Given file is not a valid zip file.'
        })
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
            f'Plugin basename cannot be "{basename}".',
            code='invalid',
        )
    for start in CANNOT_START_WITH:
        if basename.startswith(start):
            raise ValidationError(
                f'Plugin basename cannot start with "{start}".',
                code='invalid',
            )
    if f'{PLUGIN_PATH}{basename}/{basename}.py' not in file_list:
        raise ValidationError(
            'No primary file found in zip.  ' +
            'Perhaps you are attempting to upload a sub-plugin.',
            code='not-found',
        )
    return basename


def handle_plugin_zip_upload(instance, filename):
    """Return the path to store the zip for the current release."""
    slug = instance.plugin.slug
    return f'{PLUGIN_RELEASE_URL}{slug}/{slug}-v{instance.version}.zip'


def handle_plugin_logo_upload(instance, filename):
    """Return the path to store the plugin's logo."""
    extension = filename.rsplit('.', 1)[1]
    return f'{PLUGIN_LOGO_URL}{instance.slug}.{extension}'


def handle_plugin_image_upload(instance, filename):
    """Return the path to store the image."""
    slug = instance.plugin.slug
    image_number = find_image_number(
        directory='plugins',
        slug=slug,
    )
    extension = filename.rsplit('.', 1)[1]
    return f'{PLUGIN_IMAGE_URL}{slug}/{image_number}.{extension}'
