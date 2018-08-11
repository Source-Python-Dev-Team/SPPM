"""Common helper functions."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from zipfile import ZipFile, BadZipfile

# 3rd-Party Python
from configobj import ConfigObj

# Django
from django.conf import settings
from django.core.exceptions import ValidationError

# App
from project_manager.common.constants import CANNOT_BE_NAMED, CANNOT_START_WITH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'find_image_number',
    'get_file_list',
    'get_groups',
    'get_requirements',
    'handle_project_image_upload',
    'handle_project_logo_upload',
    'handle_release_zip_file_upload',
    'validate_basename',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def find_image_number(directory, slug):
    """Return the next available image number."""
    path = settings.MEDIA_ROOT / 'images' / directory / slug
    current_files = [x.namebase for x in path.files()] if path.isdir() else []
    return '%04d' % (max(map(int, current_files or [0])) + 1)


def get_groups(iterable, count=3):
    """Return lists from the given iterable in chunks of 'count'."""
    if not iterable:
        return iterable
    iterable = list(iterable)
    remainder = len(iterable) % count
    iterable.extend([''] * (count - remainder))
    return zip(*(iter(iterable),) * count)


def get_requirements(zip_file, requirement_path):
    """Return the requirements for the release."""
    for zipped_file in zip_file.filelist:
        if zipped_file.filename != requirement_path:
            continue
        ini = zip_file.open(zipped_file)
        return ConfigObj(ini)
    return {}


def handle_project_image_upload(instance, filename):
    """Handle uploading the image by directing to the proper directory."""
    return instance.handle_image_upload(filename)


def handle_project_logo_upload(instance, filename):
    """Handle uploading the logo by directing to the proper directory."""
    return instance.handle_logo_upload(filename)


def handle_release_zip_file_upload(instance, filename):
    """Handle uploading the zip file by directing to the proper directory."""
    return instance.handle_zip_file_upload(filename)


def get_file_list(zip_file):
    """Return a list of all files in the given zip file."""
    try:
        return [
            x for x in ZipFile(zip_file).namelist() if not x.endswith('/')
        ]
    except BadZipfile:
        raise ValidationError({
            'zip_file': 'Given file is not a valid zip file.'
        })


def validate_basename(basename, project_type):
    """Validate that the basename is not erroneous."""
    if basename is None:
        raise ValidationError(
            f'No base directory or file found for {project_type}.',
            code='not-found',
        )
    if basename in CANNOT_BE_NAMED:
        raise ValidationError(
            f'{project_type.capitalize()} basename cannot be "{basename}".',
            code='invalid',
        )
    for start in CANNOT_START_WITH:
        if basename.startswith(start):
            raise ValidationError(
                (
                    f'{project_type.capitalize()} basename cannot start '
                    f'with "{start}".'
                ),
                code='invalid',
            )
