"""Helpers for use with Packages."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# App
from project_manager.common.helpers import ProjectZipFile, find_image_number
from project_manager.packages.constants import (
    PACKAGE_ALLOWED_FILE_TYPES,
    PACKAGE_IMAGE_URL,
    PACKAGE_LOGO_URL,
    PACKAGE_PATH,
    PACKAGE_RELEASE_URL,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageZipFile',
    'handle_package_image_upload',
    'handle_package_logo_upload',
    'handle_package_zip_upload',
)


# =============================================================================
# CLASSES
# =============================================================================
class PackageZipFile(ProjectZipFile):
    """Package ZipFile parsing class."""

    project_type = 'Package'
    file_types = PACKAGE_ALLOWED_FILE_TYPES
    is_module = False

    def find_base_info(self):
        """Store all base information for the zip file."""
        for file_path in self.file_list:
            if not file_path.endswith('.py'):
                continue
            if not file_path.startswith(PACKAGE_PATH):
                continue

            current = file_path.split(PACKAGE_PATH, 1)[1]
            if not current:
                continue

            if '/' not in current:
                current = current.rsplit('.', 1)[0]
                self.is_module = True

            else:
                current = current.split('/', 1)[0]

            if self.basename is None:
                self.basename = current

            elif self.basename != current:
                raise ValidationError(
                    message='Multiple base directories found for package.',
                    code='multiple',
                )

    def get_base_paths(self):
        """Return a list of base paths to check against."""
        if self.is_module:
            return [f'{PACKAGE_PATH}{self.basename}.py']

        return [
            f'{PACKAGE_PATH}{self.basename}/{self.basename}.py',
            f'{PACKAGE_PATH}{self.basename}/__init__.py',
        ]

    def get_requirement_path(self):
        """Return the path for the requirements json file."""
        if self.is_module:
            return f'{PACKAGE_PATH}{self.basename}_requirements.json'
        return f'{PACKAGE_PATH}{self.basename}/requirements.json'


# =============================================================================
# FUNCTIONS
# =============================================================================
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
