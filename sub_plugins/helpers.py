# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.core.exceptions import ValidationError

# Project Imports
from plugins.constants import PLUGIN_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'get_sub_plugin_basename',
    'handle_sub_plugin_logo_upload',
    'handle_sub_plugin_zip_upload',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_sub_plugin_basename(file_list, plugin):
    plugin_name = _validate_plugin_name(file_list, plugin)
    basename = None
    path = None
    paths = [x[0] for x in plugin.paths.values_list('path')]
    for x in file_list:
        if not x.endswith('.py'):
            continue
        if not x.startswith(PLUGIN_PATH + '{0}/'.format(plugin_name)):
            continue
        current = x.split(PLUGIN_PATH + '{0}/'.format(plugin_name), 1)[1]
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
    if basename is None:
        raise ValidationError('No sub-plugin base directory found in zip.')
    return basename, path


def handle_sub_plugin_zip_upload(instance, filename):
    return 'releases/sub_plugins/{0}/{1}/{1}-v{2}.zip'.format(
        instance.plugin.basename,
        instance.basename,
        instance.version,
    )


def handle_sub_plugin_logo_upload(instance, filename):
    return 'logos/sub_plugins/{0}/{1}.{2}'.format(
        instance.plugin.basename,
        instance.basename,
        filename.rsplit('.', 1)[1]
    )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _validate_plugin_name(file_list, plugin):
    plugin_name = None
    for x in file_list:
        if not x.endswith('.py'):
            continue
        if not x.startswith(PLUGIN_PATH):
            continue
        current = x.split(PLUGIN_PATH, 1)[1]
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
