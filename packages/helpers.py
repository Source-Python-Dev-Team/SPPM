# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.core.exceptions import ValidationError

# App Imports
from .constants import PACKAGE_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'get_package_basename',
    'handle_package_logo_upload',
    'handle_package_zip_upload',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_package_basename(file_list):
    basename = None
    is_module = False
    for x in file_list:
        if not x.endswith('.py'):
            continue
        if not x.startswith(PACKAGE_PATH):
            continue
        current = x.split(PACKAGE_PATH, 1)[1]
        if not current:
            continue
        if '/' not in current:
            current = current.rsplit('.', 1)[0]
            is_module = True
        else:
            current = current.split('/', 1)[0]
        if basename is None:
            basename = current
        elif basename != current:
            raise ValidationError('Multiple base directories found for plugin')
    if basename is None:
        raise ValidationError('No base directory found for plugin.')
    return basename, is_module


def handle_package_zip_upload(instance, filename):
    return 'releases/packages/{0}/{0}-v{1}.zip'.format(
        instance.basename,
        instance.version
    )


def handle_package_logo_upload(instance, filename):
    return 'logos/packages/{0}.{1}'.format(
        instance.basename,
        filename.rsplit('.', 1)[1]
    )
