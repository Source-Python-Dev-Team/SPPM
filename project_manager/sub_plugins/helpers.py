"""Helpers for use with SubPlugins."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.core.exceptions import ValidationError

# App
from project_manager.common.helpers import ProjectZipFile, find_image_number
from project_manager.plugins.constants import PLUGIN_PATH
from project_manager.sub_plugins.constants import (
    SUB_PLUGIN_ALLOWED_FILE_TYPES,
    SUB_PLUGIN_IMAGE_URL,
    SUB_PLUGIN_LOGO_URL,
    SUB_PLUGIN_RELEASE_URL,
)


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginZipFile',
    'handle_sub_plugin_image_upload',
    'handle_sub_plugin_logo_upload',
    'handle_sub_plugin_zip_upload',
)


# =============================================================================
# CLASSES
# =============================================================================
class SubPluginZipFile(ProjectZipFile):
    """SubPlugin ZipFile parsing class."""

    project_type = 'SubPlugin'
    file_types = SUB_PLUGIN_ALLOWED_FILE_TYPES
    paths = set()
    is_module = False

    def __init__(self, zip_file, plugin):
        """Store the base attributes and the plugin."""
        self.plugin = plugin
        super().__init__(zip_file)

    def _validate_path(self, path):
        """Validate the given path is ok for the extension."""
        if self.file_types is None:
            raise NotImplementedError(
                f'File types not set for {self.__class__.__name__}.'
            )

        extension = path.rsplit('.')[1]
        if '/' in extension:
            return True

        for base_path, allowed_extensions in self.file_types.items():
            for sub_plugin_path in self.plugin.paths.values_list(
                'path',
                flat=True,
            ):
                if not path.startswith(
                    base_path.format(
                        self=self,
                        sub_plugin_path=sub_plugin_path,
                    )
                ):
                    continue
                if extension in allowed_extensions:
                    return True
                return False

        return False

    def find_base_info(self):
        """Store all base information for the zip file."""
        plugin_path = f'{PLUGIN_PATH}{self.plugin.basename}/'
        paths = list(self.plugin.paths.values_list('path', flat=True))
        for file_path in self.file_list:
            if not file_path.endswith('.py'):
                continue

            if not file_path.startswith(plugin_path):
                # TODO: validate not another plugin path or package
                continue

            current = file_path.split(plugin_path, 1)[1]
            if not current:
                continue

            for current_path in paths:
                if not current.startswith(current_path):
                    continue

                current = current.split(current_path, 1)[1]
                if current.startswith('/'):
                    current = current[1:]

                current = current.split('/', 1)[0]
                if not current:
                    continue

                if self.basename is None:
                    self.basename = current

                elif self.basename != current:
                    raise ValidationError(
                        message='Multiple sub-plugins found in zip.',
                        code='multiple',
                    )

                self.paths.add(current_path)

    def validate_base_file_in_zip(self):
        """Verify that there is a base file within the zip file."""
        plugin_paths = {
            values['path']: {
                'allow_module': values['allow_module'],
                'allow_package_using_basename': values[
                    'allow_package_using_basename'
                ],
                'allow_package_using_init': values['allow_package_using_init'],
            } for values in self.plugin.paths.filter(
                path__in=self.paths,
            ).values(
                'path',
                'allow_module',
                'allow_package_using_basename',
                'allow_package_using_init',
            )
        }
        for path in self.paths:
            self._validate_base_file_in_zip(
                base_path=path,
                path_values=plugin_paths[path]
            )

    def _validate_base_file_in_zip(self, base_path, path_values):
        """Verify a base file is found in the given path."""
        if not base_path.startswith('/'):
            base_path = '/' + base_path
        if not base_path.endswith('/'):
            base_path += '/'
        sub_path = f'{PLUGIN_PATH}{self.plugin.basename}{base_path}'
        module_found = package_found = False
        if path_values['allow_module']:
            check_path = f'{sub_path}{self.basename}.py'
            self.is_module = module_found = check_path in self.file_list

        if path_values['allow_package_using_basename']:
            check_path = f'{sub_path}{self.basename}/{self.basename}.py'
            package_found = check_path in self.file_list

        if path_values['allow_package_using_init']:
            check_path = f'{sub_path}{self.basename}/__init__.py'
            package_found = check_path in self.file_list or package_found

        if package_found and module_found:
            raise ValidationError(
                message=(
                    f'SubPlugin found as both a module and package in the same'
                    f' path: "{sub_path}".'
                )
            )

        if package_found or module_found:
            return

        raise ValidationError(
            message=(
                f'SubPlugin not found in path, though files found within zip '
                f'for directory: "{sub_path}".'
            )
        )

    def get_requirement_path(self):
        """Return the path for the requirements json file."""
        if self.is_module:
            return (
                f'{PLUGIN_PATH}{self.plugin.basename}/'
                f'{self.basename}_requirements.json'
            )
        return (
            f'{PLUGIN_PATH}{self.plugin.basename}/'
            f'{self.basename}/requirements.json'
        )


# =============================================================================
# FUNCTIONS
# =============================================================================
def handle_sub_plugin_zip_upload(instance, filename):
    """Return the path to store the zip for the current release."""
    slug = instance.sub_plugin.slug
    return (
        f'{SUB_PLUGIN_RELEASE_URL}{instance.sub_plugin.plugin.slug}/{slug}/'
        f'{slug}-v{instance.version}.zip'
    )


def handle_sub_plugin_logo_upload(instance, filename):
    """Return the path to store the sub-plugin's logo."""
    extension = filename.rsplit('.', 1)[1]
    return (
        f'{SUB_PLUGIN_LOGO_URL}{instance.plugin.slug}/'
        f'{instance.slug}.{extension}'
    )


def handle_sub_plugin_image_upload(instance, filename):
    """Return the path to store the image."""
    plugin_slug = instance.sub_plugin.plugin.slug
    slug = instance.sub_plugin.slug
    image_number = find_image_number(
        directory=f'sub-plugins/{plugin_slug}',
        slug=slug,
    )
    extension = filename.rsplit('.', 1)[1]
    return (
        f'{SUB_PLUGIN_IMAGE_URL}{plugin_slug}/{slug}/'
        f'{image_number}.{extension}'
    )
