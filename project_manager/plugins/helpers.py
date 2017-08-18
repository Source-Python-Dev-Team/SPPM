"""Helpers for use with Plugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# App
from project_manager.common.helpers import (
    find_image_number,
    get_file_list,
    validate_basename,
)
from .constants import (
    PLUGIN_PATH, PLUGIN_IMAGE_URL, PLUGIN_LOGO_URL, PLUGIN_RELEASE_URL,
)


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
    file_list = get_file_list(zip_file)
    basename = _find_basename(file_list)
    validate_basename(basename=basename, project_type='plugin')
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


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _find_basename(file_list):
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
    return basename
