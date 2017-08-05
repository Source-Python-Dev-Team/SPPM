# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from zipfile import ZipFile, BadZipfile

# Django
from django.core.exceptions import ValidationError

# App
from .constants import (
    PACKAGE_PATH, PACKAGE_IMAGE_URL, PACKAGE_LOGO_URL, PACKAGE_RELEASE_URL,
)
from project_manager.common.constants import CANNOT_BE_NAMED, CANNOT_START_WITH
from project_manager.common.helpers import find_image_number


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
def get_package_basename(zip_file):
    """Return the package's basename."""
    # TODO: add module/package validation
    try:
        file_list = [
            x for x in ZipFile(zip_file).namelist() if not x.endswith('/')
        ]
    except BadZipfile:
        raise ValidationError({
            'zip_file': 'Given file is not a valid zip file.'
        })
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
                'Multiple base directories found for package.',
                code='multiple',
            )
    if basename is None:
        raise ValidationError(
            'No base directory or file found for package.',
            code='not-found',
        )
    if basename in CANNOT_BE_NAMED:
        raise ValidationError(
            f'Package basename cannot be "{basename}".',
            code='invalid',
        )
    for start in CANNOT_START_WITH:
        if basename.startswith(start):
            raise ValidationError(
                f'Package basename cannot start with "{start}".',
                code='invalid',
            )
    return basename, is_module


def handle_package_zip_upload(instance, filename):
    """Return the path to store the zip for the current release."""
    slug = instance.package.slug,
    version = instance.version,
    return f'{PACKAGE_RELEASE_URL}{slug}/{slug}-v{version}.zip'


def handle_package_logo_upload(instance, filename):
    """Return the path to store the package's logo."""
    extension = filename.rsplit('.', 1)[1],
    return f'{PACKAGE_LOGO_URL}{instance.slug}.{extension}'


def handle_package_image_upload(instance, filename):
    """Return the path to store the image."""
    slug = instance.package.slug,
    image_number = find_image_number('packages', instance.package.slug),
    extension = filename.rsplit('.', 1)[1],
    return f'{PACKAGE_IMAGE_URL}{slug}/{image_number}.{extension}'
