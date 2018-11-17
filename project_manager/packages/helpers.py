"""Helpers for use with Packages."""

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
from project_manager.packages.constants import (
    PACKAGE_PATH,
    PACKAGE_IMAGE_URL,
    PACKAGE_LOGO_URL,
    PACKAGE_RELEASE_URL,
)


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
    file_list = get_file_list(zip_file)
    basename, is_module = _find_basename_and_is_module(file_list)
    validate_basename(basename=basename, project_type='package')
    return basename


def handle_package_zip_upload(instance, filename):
    """Return the path to store the zip for the current release."""
    slug = instance.package.slug
    return f'{PACKAGE_RELEASE_URL}{slug}/{slug}-v{instance.version}.zip'


def handle_package_logo_upload(instance, filename):
    """Return the path to store the package's logo."""
    extension = filename.rsplit('.', 1)[1]
    return f'{PACKAGE_LOGO_URL}{instance.slug}.{extension}'


def handle_package_image_upload(instance, filename):
    """Return the path to store the image."""
    slug = instance.package.slug
    image_number = find_image_number(
        directory='packages',
        slug=slug,
    )
    extension = filename.rsplit('.', 1)[1]
    return f'{PACKAGE_IMAGE_URL}{slug}/{image_number}.{extension}'


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _find_basename_and_is_module(file_list):
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
    return basename, is_module
