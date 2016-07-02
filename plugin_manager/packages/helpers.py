# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# App
from .constants import (
    PACKAGE_PATH, PACKAGE_IMAGE_URL, PACKAGE_LOGO_URL, PACKAGE_RELEASE_URL,
)
from ..common.constants import CANNOT_BE_NAMED, CANNOT_START_WITH
from ..common.helpers import find_image_number


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
    for file_path in file_list:
        if not file_path.endswith('.py'):
            continue
        if not file_path.startswith(PACKAGE_PATH):
            continue
        current = file_path.split(PACKAGE_PATH, 1)[1]
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
            'Package basename cannot be "{basename}".'.format(
                basename=basename
            )
        )
    for start in CANNOT_START_WITH:
        if basename.startswith(start):
            raise ValidationError(
                'Package basename cannot start with "{start}".'.format(
                    start=start,
                )
            )
    return basename, is_module


def handle_package_zip_upload(instance, filename):
    """Return the path to store the zip for the current release."""
    return '{release_url}{basename}/{basename}-v{version}.zip'.format(
        release_url=PACKAGE_RELEASE_URL,
        basename=instance.basename,
        version=instance.version,
    )


def handle_package_logo_upload(instance, filename):
    """Return the path to store the package's logo."""
    return '{logo_url}{basename}.{extension}'.format(
        logo_url=PACKAGE_LOGO_URL,
        basename=instance.basename,
        extension=filename.rsplit('.', 1)[1],
    )


def handle_package_image_upload(instance, filename):
    """Return the path to store the image."""
    return '{image_url}{basename}/{image_number}.{extension}'.format(
        image_url=PACKAGE_IMAGE_URL,
        basename=instance.package.basename,
        image_number=find_image_number('packages', instance.package.basename),
        extension=filename.rsplit('.', 1)[1],
    )
