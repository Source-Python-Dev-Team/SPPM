from django.core.exceptions import ValidationError

from .constants import PLUGIN_PATH


__all__ = (
    'get_plugin_basename',
    'handle_plugin_upload',
)


def get_plugin_basename(file_list):
    basename = None
    for x in file_list:
        if not x.endswith('.py'):
            continue
        if not x.startswith(PLUGIN_PATH):
            continue
        current = x.split(PLUGIN_PATH, 1)[1]
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
    return basename


def handle_plugin_upload(instance, filename):
    return 'releases/plugins/{0}/{0}-v{1}.zip'.format(
        instance.basename,
        instance.version,
    )
