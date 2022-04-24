"""Helpers for use with Plugins."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# App
from project_manager.helpers import ProjectZipFile, find_image_number
from project_manager.plugins.constants import (
    PLUGIN_ALLOWED_FILE_TYPES,
    PLUGIN_IMAGE_URL,
    PLUGIN_LOGO_URL,
    PLUGIN_PATH,
    PLUGIN_RELEASE_URL,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginZipFile',
    'handle_plugin_image_upload',
    'handle_plugin_logo_upload',
    'handle_plugin_zip_upload',
)


# =============================================================================
# CLASSES
# =============================================================================
class PluginZipFile(ProjectZipFile):
    """Plugin ZipFile parsing class."""

    project_type = 'Plugin'
    file_types = PLUGIN_ALLOWED_FILE_TYPES

    def find_base_info(self):
        """Store all base information for the zip file."""
        for file_path in self.file_list:
            if not file_path.startswith(PLUGIN_PATH):
                continue

            current = file_path.split(PLUGIN_PATH, 1)[1]
            if not current:
                continue

            if not file_path.endswith('.py'):
                continue

            current = current.split('/', 1)[0]

            if self.basename is None:
                self.basename = current
            elif self.basename != current:
                raise ValidationError(
                    message='Multiple base directories found for plugin.',
                    code='multiple',
                )

    def get_base_paths(self):
        """Return a list of base paths to check against."""
        return [f'{PLUGIN_PATH}{self.basename}/{self.basename}.py']

    def get_requirement_path(self):
        """Return the path for the requirements json file."""
        return f'{PLUGIN_PATH}{self.basename}/requirements.json'


# =============================================================================
# FUNCTIONS
# =============================================================================
def handle_plugin_zip_upload(instance):
    """Return the path to store the zip for the current release."""
    slug = instance.plugin.slug
    return f'{PLUGIN_RELEASE_URL}{slug}/{slug}-v{instance.version}.zip'


def handle_plugin_logo_upload(instance, filename):
    """Return the path to store the plugin's logo."""
    extension = filename.rsplit('.', 1)[1]
    return f'{PLUGIN_LOGO_URL}{instance.slug}.{extension}'


def handle_plugin_image_upload(instance, filename):
    """Return the path to store the image."""
    slug = instance.plugin.slug
    image_number = find_image_number(
        directory='plugins',
        slug=slug,
    )
    extension = filename.rsplit('.', 1)[1]
    return f'{PLUGIN_IMAGE_URL}{slug}/{image_number}.{extension}'
