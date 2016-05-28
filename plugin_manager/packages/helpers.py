# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.core.exceptions import ValidationError

# Project Imports
from ..common.constants import CANNOT_BE_NAMED, CANNOT_START_WITH
from ..common.helpers import find_image_number

# App Imports
from .constants import PACKAGE_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'get_package_basename',
    'handle_package_image_upload',
    'handle_package_logo_upload',
    'handle_package_zip_upload',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_package_basename(file_list):
    """Return the package's basename."""
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
            raise ValidationError(
                'Multiple base directories found for package.')
    if basename is None:
        raise ValidationError('No base directory or file found for package.')
    if basename in CANNOT_BE_NAMED:
        raise ValidationError(
            'Package basename cannot be "{0}".'.format(basename))
    if basename.startswith(CANNOT_START_WITH):
        raise ValidationError(
            'Package basename cannot start with "{0}".'.format(basename))
    return basename, is_module


def handle_package_zip_upload(instance, filename):
    """Return the path to store the zip for the current release."""
    return 'releases/packages/{0}/{0}-v{1}.zip'.format(
        instance.basename,
        instance.version,
    )


def handle_package_logo_upload(instance, filename):
    """Return the path to store the package's logo."""
    return 'logos/packages/{0}.{1}'.format(
        instance.basename,
        filename.rsplit('.', 1)[1],
    )


def handle_package_image_upload(instance, filename):
    """Return the path to store the image."""
    return 'images/packages/{0}/{1}.{2}'.format(
        instance.package.basename,
        find_image_number('packages', instance.package.basename),
        filename.rsplit('.', 1)[1],
    )
