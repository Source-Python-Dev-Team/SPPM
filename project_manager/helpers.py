"""Common helper functions."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
import json
import logging
from collections import defaultdict
from zipfile import ZipFile, BadZipFile

# Django
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError

# App
from project_manager.constants import CANNOT_BE_NAMED, CANNOT_START_WITH


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'GROUP_QUERYSET_NAMES',
    'ProjectZipFile',
    'find_image_number',
    'handle_project_logo_upload',
    'handle_release_zip_file_upload',
)


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
DownloadRequirement = apps.get_model(
    app_label='requirements',
    model_name='DownloadRequirement',
)
PyPiRequirement = apps.get_model(
    app_label='requirements',
    model_name='PyPiRequirement',
)
VersionControlRequirement = apps.get_model(
    app_label='requirements',
    model_name='VersionControlRequirement',
)
logger = logging.getLogger(__name__)
GROUP_QUERYSET_NAMES = {
    'custom': 'package',
    'pypi': 'pypi',
    'vcs': 'versioncontrol',
    'download': 'download',
}


# =============================================================================
# CLASSES
# =============================================================================
class ProjectZipFile:
    """Base ZipFile parsing class."""

    def __init__(self, zip_file):
        """Store the base attributes for the zip file."""
        self.zip_file = zip_file
        with ZipFile(self.zip_file) as zip_obj:
            self.file_list = self.get_file_list(zip_obj)
        self.basename = None
        self.requirements = defaultdict(list)
        self.requirements_errors = []

    @property
    def project_type(self):
        """Return the type of project."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            f'"project_type" attribute.'
        )

    @property
    def file_types(self):
        """Return the type of project."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            f'"file_types" attribute.'
        )

    def find_base_info(self):
        """Store all base information for the zip file."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            f'"find_base_info" method.'
        )

    def get_base_paths(self):
        """Return a list of base paths to check against."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            f'"get_base_paths" method.'
        )

    def validate_file_paths(self):
        """Validate all paths in the zip file for their extension."""
        invalid_paths = []
        for file_path in self.file_list:
            if not self._validate_path(file_path):
                invalid_paths.append(file_path)

        if invalid_paths:
            raise ValidationError({
                'zip_file': (
                    f'Invalid paths found in zip: {", ".join(invalid_paths)}'
                )
            })

    def _validate_path(self, path):
        """Validate the given path is ok for the extension."""
        if path.endswith('/'):
            return True

        try:
            extension = path.rsplit('/', 1)[1].rsplit('.', 1)[1]
        except IndexError:
            return True

        for base_path, allowed_extensions in self.file_types.items():
            if not path.startswith(base_path.format(self=self)):
                continue

            # extension allowed for path
            if extension in allowed_extensions:
                return True

            # extension not allowed for path
            return False

        # File not found in any allowed paths
        return False

    @staticmethod
    def get_file_list(zip_obj):
        """Return a list of all files in the given zip file."""
        try:
            return [x for x in zip_obj.namelist() if not x.endswith('/')]
        except BadZipFile as exception:
            raise ValidationError({
                'zip_file': 'Given file is not a valid zip file.'
            }) from exception

    def validate_basename(self):
        """Validate that the basename is not erroneous."""
        if self.basename is None:
            raise ValidationError(
                message=(
                    f'No base directory or file found for {self.project_type}.'
                ),
                code='not-found',
            )
        if self.basename in CANNOT_BE_NAMED:
            raise ValidationError(
                message=(
                    f'{self.project_type} basename cannot be '
                    f'"{self.basename}".'
                ),
                code='invalid',
            )
        for start in CANNOT_START_WITH:
            if self.basename.startswith(start):
                raise ValidationError(
                    message=(
                        f'{self.project_type} basename cannot start with '
                        f'"{start}".'
                    ),
                    code='invalid',
                )

    def validate_base_file_in_zip(self):
        """Verify that there is a base file within the zip file."""
        for path in self.get_base_paths():
            if path in self.file_list:
                break
        else:
            raise ValidationError(
                message='No primary file found in zip.',
                code='not-found',
            )

    def validate_requirements(self):
        """Return the requirements for the release."""
        contents = self.get_requirements_file_contents()
        if contents is None:
            return

        for group_type, group in contents.items():
            if group_type not in GROUP_QUERYSET_NAMES:
                self.requirements_errors.append(
                    f'Invalid group name "{group_type}" found in '
                    f'requirements json file.'
                )
                continue

            if not isinstance(group, list):
                self.requirements_errors.append(
                    f'Invalid group values for "{group_type}" found in '
                    f'requirements json file.'
                )
                continue

            for item in group:
                if not isinstance(item, dict):
                    self.requirements_errors.append(
                        f'Invalid object found in "{group_type}" listing in '
                        f'requirements json file.'
                    )
                    continue

                if group_type == 'custom':
                    self._validate_custom_requirement(
                        item=item,
                    )
                else:
                    is_pypi = group_type == 'pypi'
                    self._validate_requirement(
                        item=item,
                        group_type=group_type,
                        field='name' if is_pypi else 'url',
                        include_version=is_pypi,
                    )

        if self.requirements_errors:
            raise ValidationError({
                'zip_file': self.requirements_errors,
            })

    def get_requirements_file_contents(self):
        """Return the contents of the requirements.json file."""
        requirement_path = self.get_requirement_path()
        try:
            with ZipFile(self.zip_file).open(requirement_path) as requirement_file:
                contents = json.load(requirement_file)
        except KeyError:
            logger.debug('No requirement file found.')
            return None
        except json.decoder.JSONDecodeError as exception:
            raise ValidationError({
                'zip_file': 'Requirements json file cannot be decoded.'
            }) from exception

        if not isinstance(contents, dict):
            raise ValidationError({
                'zip_file': 'Invalid requirements json file.'
            })

        return contents

    def get_requirement_path(self):
        """Return the path for the requirements json file."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            f'"get_requirement_path" method.'
        )

    def _validate_custom_requirement(self, item):
        """Verify that the given requirement exists."""
        basename = item.get('basename')
        if basename is None:
            self.requirements_errors.append(
                'No basename found for object in "custom" '
                'listing in requirements json file.'
            )
            return

        package_model = apps.get_model(
            app_label='project_manager',
            model_name='Package',
        )
        try:
            package = package_model.objects.get(basename=basename)
        except package_model.DoesNotExist:
            self.requirements_errors.append(
                f'Custom Package "{basename}" from requirements '
                f'json file not found.'
            )
            return

        version = item.get('version')
        # TODO: update this logic to work with all version operators
        if (
            version is not None and
            not package.releases.filter(version=version).exists()
        ):
            self.requirements_errors.append(
                f'Custom Package "{basename}" version "{version}", '
                f'from requirements json file, not found.'
            )
            return

        self.requirements['custom'].append({
            'package_requirement': package,
            'version': version,
            'optional': item.get('optional', False),
        })

    def _validate_requirement(
        self, item, group_type, field, include_version=False
    ):
        """Verify that the given requirement is valid."""
        # TODO: validate pypi requirements?
        # TODO: validate vcs requirements?
        model = {
            'download': DownloadRequirement,
            'pypi': PyPiRequirement,
            'vcs': VersionControlRequirement,
        }.get(group_type)
        value = item.get(field)
        if value is None:
            self.requirements_errors.append(
                f'No {field} found for object in "{group_type}" listing in '
                f'requirements json file.'
            )
            return

        instance, created = model.objects.get_or_create(**{field: value})
        key = f'{group_type}_requirement'
        requirement_dict = {
            key: instance,
            'optional': item.get('optional', False),
        }
        if include_version:
            requirement_dict.update({
                'version': item.get('version'),
            })

        self.requirements[group_type].append(requirement_dict)


# =============================================================================
# FUNCTIONS
# =============================================================================
def find_image_number(directory, slug):
    """Return the next available image number."""
    path = settings.MEDIA_ROOT / 'images' / directory / slug
    current_files = [x.stem for x in path.files()] if path.isdir() else []
    return f'{max(map(int, current_files or [0])) + 1:04}'


def handle_project_logo_upload(instance, filename):
    """Handle uploading the logo by directing to the proper directory."""
    return instance.handle_logo_upload(filename)


def handle_release_zip_file_upload(instance, filename):
    """Handle uploading the zip file by directing to the proper directory."""
    return instance.handle_zip_file_upload()
