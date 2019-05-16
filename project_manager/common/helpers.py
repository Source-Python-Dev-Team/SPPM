"""Common helper functions."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import json
from zipfile import ZipFile, BadZipfile

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
    try:
        with zip_file.open(requirement_path) as requirement_file:
            contents = json.load(requirement_file)
    except KeyError:
        return {}
    except json.JSONDecodeError:
        raise ValidationError({
            'zip_file': 'Requirements json file cannot be decoded.'
        })
    if not isinstance(contents, dict):
        raise ValidationError({
            'zip_file': 'Invalid requirements json file.'
        })
    requirements = {
        'custom': [],
        'pypi': [],
        'vcs': [],
        'download': [],
    }
    errors = []
    for group_type, group in contents.items():
        if group_type not in requirements:
            errors.append(
                f'Invalid group name "{group_type} found in requirements '
                f'json file.'
            )
            continue
        if not isinstance(group, list):
            errors.append(
                f'Invalid group values for "{group_type}" found in '
                f'requirements json file.'
            )
            continue
        for item in group:
            if not isinstance(item, dict):
                errors.append(
                    f'Invalid object found in "{group_type}" listing in '
                    f'requirements json file.'
                )
                continue
            if group_type == 'custom':
                _validate_custom_requirement(
                    item=item,
                    custom_requirements=requirements[group_type],
                    errors=errors,
                )
            elif group_type == 'pypi':
                _validate_requirement(
                    item=item,
                    group_requirements=requirements[group_type],
                    group_type=group_type,
                    field='name',
                    errors=errors,
                    include_version=True,
                )
            else:
                _validate_requirement(
                    item=item,
                    group_requirements=requirements[group_type],
                    group_type=group_type,
                    field='url',
                    errors=errors,
                )
    if errors:
        raise ValidationError({
            'zip_file': errors,
        })
    return requirements


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


def _validate_custom_requirement(item, custom_requirements, errors):
    from project_manager.packages.models import Package
    basename = item.get('basename')
    if basename is None:
        errors.append(
            f'No basename found for object in "custom" '
            f'listing in requirements json file.'
        )
        return
    try:
        package = Package.objects.get(basename=basename)
    except Package.DoesNotExist:
        errors.append(
            f'Custom Package "{basename}" from requirements '
            f'json file not found.'
        )
        return
    version = item.get('version')
    # TODO: update this logic to work with all version operators
    available_versions = package.releases.values_list(
        'version',
        flat=True,
    )
    if version is not None and version not in available_versions:
        errors.append(
            f'Custom Package "{basename}" version "{version}", '
            f'from requirements json file, not found.'
        )
        return
    custom_requirements.append({
        'basename': basename,
        'version': version,
        'optional': item.get('optional', False),
    })


def _validate_requirement(
    item, group_requirements, group_type, field, errors, include_version=False
):
    value = item.get(field)
    if value is None:
        errors.append(
            f'No {field} found for object in "{group_type}" listing in '
            f'requirements json file.'
        )
        return
    requirement_dict = {
        field: value,
        'optional': item.get('optional', False),
    }
    if include_version:
        requirement_dict.update({
            'version': item.get('version'),
        })
    group_requirements.append(requirement_dict)
