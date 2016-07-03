# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# App
from .constants import (
    SUB_PLUGIN_IMAGE_URL, SUB_PLUGIN_LOGO_URL, SUB_PLUGIN_RELEASE_URL,
)
from ..plugins.constants import PLUGIN_PATH
from ..common.constants import CANNOT_BE_NAMED, CANNOT_START_WITH
from ..common.helpers import find_image_number


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'get_sub_plugin_basename',
    'handle_sub_plugin_image_upload',
    'handle_sub_plugin_logo_upload',
    'handle_sub_plugin_zip_upload',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_sub_plugin_basename(file_list, plugin):
    """Return the sub-plugin's basename."""
    basename, path = _find_basename_and_path(file_list, plugin)
    if basename is None:
        raise ValidationError('No sub-plugin base directory found in zip.')
    if basename in CANNOT_BE_NAMED:
        raise ValidationError(
            'Sub-plugin basename cannot be "{basename}".'.format(
                basename=basename,
            )
        )
    for start in CANNOT_START_WITH:
        if basename.startswith(start):
            raise ValidationError(
                'Sub-plugin basename cannot start with "{start}".'.format(
                    start=start,
                )
            )
    return basename, path


def handle_sub_plugin_zip_upload(instance, filename):
    """Return the path to store the zip for the current release."""
    return (
        '{release_url}{plugin_slug}/{slug}/'
        '{slug}-v{version}.zip'.format(
            release_url=SUB_PLUGIN_RELEASE_URL,
            plugin_slug=instance.sub_plugin.plugin.slug,
            slug=instance.sub_plugin.slug,
            version=instance.version,
        )
    )


def handle_sub_plugin_logo_upload(instance, filename):
    """Return the path to store the sub-plugin's logo."""
    return '{logo_url}{plugin_slug}/{slug}.{extension}'.format(
        logo_url=SUB_PLUGIN_LOGO_URL,
        plugin_slug=instance.plugin.slug,
        slug=instance.slug,
        extension=filename.rsplit('.', 1)[1],
    )


def handle_sub_plugin_image_upload(instance, filename):
    """Return the path to store the image."""
    return (
        '{image_url}{plugin_slug}/{slug}/'
        '{image_number}.{extension}'.format(
            image_url=SUB_PLUGIN_IMAGE_URL,
            plugin_slug=instance.sub_plugin.plugin.slug,
            slug=instance.sub_plugin.slug,
            image_number=find_image_number(
                'sub_plugins/{plugin_basename}'.format(
                    plugin_basename=instance.sub_plugin.plugin.slug,
                ),
                instance.sub_plugin.slug,
            ),
            extension=filename.rsplit('.', 1)[1],
        )
    )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _validate_plugin_name(file_list, plugin):
    """Return the username of the plugin."""
    plugin_name = None
    for file_path in file_list:
        if not file_path.endswith('.py'):
            continue
        if not file_path.startswith(PLUGIN_PATH):
            continue
        current = file_path.split(PLUGIN_PATH, 1)[1]
        if not current:
            continue
        current = current.split('/', 1)[0]
        if plugin_name is None:
            plugin_name = current
        elif plugin_name != current:
            raise ValidationError('Multiple plugins found in zip.')
    if plugin_name is None:
        raise ValidationError('No plugin base directory found in zip.')
    if plugin_name != plugin.basename:
        raise ValidationError('Wrong plugin base directory found in zip.')
    return plugin_name


def _find_basename_and_path(file_list, plugin):
    plugin_name = _validate_plugin_name(file_list, plugin)
    path = None
    paths = [x[0] for x in plugin.paths.values_list('path')]
    basename = None
    for file_path in file_list:
        if not file_path.endswith('.py'):
            continue
        file_path_start = '{plugin_path}{plugin_name}/'.format(
            plugin_path=PLUGIN_PATH,
            plugin_name=plugin_name,
        )
        if not file_path.startswith(file_path_start):
            continue
        current = file_path.split(file_path_start, 1)[1]
        if not current:
            continue
        for current_path in paths:
            if not current.startswith(current_path):
                continue
            current = current.split(current_path, 1)[1]
            if current.startswith('/'):
                current = current[1:]
            current = current.split('/', 1)[0]
            if not current:
                continue
            if basename is None:
                basename = current
                path = current_path
            elif basename != current:
                raise ValidationError('Multiple sub-plugins found in zip.')
    return basename, path
