# =============================================================================
# IMPORTS
# =============================================================================
# Python
from random import randint
from unittest import mock

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase

# App
from project_manager.common.helpers import ProjectZipFile
from project_manager.plugins.constants import PLUGIN_PATH
from project_manager.sub_plugins.constants import (
    SUB_PLUGIN_ALLOWED_FILE_TYPES,
    SUB_PLUGIN_IMAGE_URL,
    SUB_PLUGIN_LOGO_URL,
    SUB_PLUGIN_RELEASE_URL,
)
from project_manager.sub_plugins.helpers import (
    SubPluginZipFile,
    handle_sub_plugin_image_upload,
    handle_sub_plugin_logo_upload,
    handle_sub_plugin_zip_upload,
)
from test_utils.factories.packages import PackageReleaseFactory, PackageFactory
from test_utils.factories.plugins import PluginFactory, SubPluginPathFactory
from test_utils.factories.requirements import (
    VersionControlRequirementFactory,
    PyPiRequirementFactory,
    DownloadRequirementFactory,
)
from test_utils.factories.sub_plugins import (
    SubPluginFactory,
    SubPluginImageFactory,
    SubPluginReleaseFactory,
)


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginZipFileTestCase(TestCase):

    base_path = plugin = sub_plugin_path = None

    @classmethod
    def setUpTestData(cls):
        cls.plugin = PluginFactory()
        cls.sub_plugin_path = SubPluginPathFactory(
            plugin=cls.plugin,
            path='sub_plugins',
            allow_package_using_basename=True,
        )
        SubPluginPathFactory(
            plugin=cls.plugin,
            path='other_path',
        )
        cls.base_path = f'{PLUGIN_PATH}{cls.plugin.basename}/sub_plugins/'

    def setUp(self) -> None:
        super().setUp()
        self.mock_get_file_list = mock.patch(
            target='project_manager.common.helpers.ProjectZipFile.get_file_list',
        ).start()

    def tearDown(self) -> None:
        super().tearDown()
        mock.patch.stopall()

    def _get_file_list(self, sub_plugin_basename):
        base_path = f'{self.base_path}{sub_plugin_basename}'
        return tuple(
            reversed([
                base_path.rsplit('/', i)[0] + '/'
                for i in range(1, base_path.count('/') + 1)
            ])
        ) + (
            f'{base_path}',
            f'{base_path}/__init__.py',
            f'{base_path}/{sub_plugin_basename}.py',
            f'{base_path}/{sub_plugin_basename}/helpers.py',
            f'{base_path}/{sub_plugin_basename}/requirements.json',
        )

    def _get_module_file_list(self, sub_plugin_basename):
        return tuple(
            reversed([
                self.base_path.rsplit('/', i)[0] + '/'
                for i in range(1, self.base_path.count('/') + 1)
            ])
        ) + (
            f'{self.base_path}{sub_plugin_basename}.py',
            f'{self.base_path}{sub_plugin_basename}_requirements.json',
        )

    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginZipFile, ProjectZipFile))

    def test_project_type(self):
        self.assertEqual(
            first=SubPluginZipFile.project_type,
            second='SubPlugin',
        )

    def test_file_types(self):
        self.assertDictEqual(
            d1=SubPluginZipFile.file_types,
            d2=SUB_PLUGIN_ALLOWED_FILE_TYPES,
        )

    @mock.patch(
        target='project_manager.common.helpers.ZipFile',
    )
    def test_find_base_info(self, _):
        sub_plugin_basename = 'test_sub_plugin'
        self.mock_get_file_list.return_value = self._get_file_list(
            sub_plugin_basename=sub_plugin_basename,
        )
        obj = SubPluginZipFile('', self.plugin)
        obj.find_base_info()
        self.assertEqual(
            first=obj.basename,
            second=sub_plugin_basename,
        )

        self.mock_get_file_list.return_value += (
            f'{self.base_path}second_basename/__init__.py',
        )
        with self.assertRaises(ValidationError) as context:
            obj = SubPluginZipFile('', self.plugin)
            obj.find_base_info()

        self.assertEqual(
            first=context.exception.message,
            second='Multiple sub-plugins found in zip.',
        )
        self.assertEqual(
            first=context.exception.code,
            second='multiple',
        )

    @mock.patch(
        target='project_manager.common.helpers.ZipFile',
    )
    def test_validate_base_file_in_zip(self, _):
        sub_plugin_basename = 'test_plugin'
        self.mock_get_file_list.return_value = self._get_file_list(
            sub_plugin_basename=sub_plugin_basename,
        )
        obj = SubPluginZipFile('', self.plugin)
        obj.find_base_info()
        obj.validate_base_file_in_zip()

        self.sub_plugin_path.allow_package_using_basename = False
        self.sub_plugin_path.allow_package_using_init = True
        self.sub_plugin_path.save()
        obj = SubPluginZipFile('', self.plugin)
        obj.find_base_info()
        obj.validate_base_file_in_zip()

        self.sub_plugin_path.allow_package_using_init = False
        self.sub_plugin_path.allow_module = True
        self.sub_plugin_path.save()
        self.mock_get_file_list.return_value = self._get_module_file_list(
            sub_plugin_basename=sub_plugin_basename,
        )
        obj = SubPluginZipFile('', self.plugin)
        obj.find_base_info()
        obj.validate_base_file_in_zip()
        self.assertTrue(expr=obj.is_module)

        self.sub_plugin_path.allow_package_using_basename = True
        self.sub_plugin_path.save()
        self.mock_get_file_list.return_value = self._get_file_list(
            sub_plugin_basename=sub_plugin_basename,
        ) + self._get_module_file_list(
            sub_plugin_basename=sub_plugin_basename,
        )
        obj = SubPluginZipFile('', self.plugin)
        obj.find_base_info()
        with self.assertRaises(ValidationError) as context:
            obj.validate_base_file_in_zip()

        self.assertEqual(
            first=context.exception.message,
            second=(
                f'SubPlugin found as both a module and package in the same '
                f'path: "{self.base_path}".'
            ),
        )
        self.assertEqual(
            first=context.exception.code,
            second='invalid',
        )

        obj.basename = 'invalid'
        with self.assertRaises(ValidationError) as context:
            obj.validate_base_file_in_zip()

        self.assertEqual(
            first=context.exception.message,
            second=(
                f'SubPlugin not found in path, though files found within zip '
                f'for directory: "{self.base_path}".'
            ),
        )
        self.assertEqual(
            first=context.exception.code,
            second='not-found',
        )

    @mock.patch(
        target='project_manager.common.helpers.ZipFile',
    )
    def test_get_requirement_paths(self, _):
        sub_plugin_basename = 'test_sub_plugin'
        self.mock_get_file_list.return_value = self._get_file_list(
            sub_plugin_basename=sub_plugin_basename,
        )
        obj = SubPluginZipFile('', self.plugin)
        obj.find_base_info()
        obj.validate_base_file_in_zip()
        self.assertListEqual(
            list1=obj.get_requirement_paths(),
            list2=[
                f'{PLUGIN_PATH}{self.plugin.basename}/{self.sub_plugin_path.path}/'
                f'{sub_plugin_basename}/requirements.json'
            ],
        )

        self.sub_plugin_path.allow_package_using_basename = False
        self.sub_plugin_path.allow_module = True
        self.sub_plugin_path.save()
        self.mock_get_file_list.return_value = self._get_module_file_list(
            sub_plugin_basename=sub_plugin_basename,
        )
        obj = SubPluginZipFile('', self.plugin)
        obj.find_base_info()
        obj.validate_base_file_in_zip()
        self.assertListEqual(
            list1=obj.get_requirement_paths(),
            list2=[
                f'{PLUGIN_PATH}{self.plugin.basename}/{self.sub_plugin_path.path}/'
                f'{sub_plugin_basename}_requirements.json'
            ],
        )

    @mock.patch(
        target='project_manager.common.helpers.ZipFile',
    )
    def test_validate_file_paths(self, _):
        sub_plugin_basename = 'test_plugin'
        self.mock_get_file_list.return_value = self._get_file_list(
            sub_plugin_basename=sub_plugin_basename,
        )
        obj = SubPluginZipFile('', self.plugin)
        obj.find_base_info()
        obj.validate_base_file_in_zip()
        obj.validate_file_paths()

        invalid_file = f'{self.base_path}{sub_plugin_basename}/{sub_plugin_basename}.invalid'
        self.mock_get_file_list.return_value = self._get_file_list(
            sub_plugin_basename=sub_plugin_basename,
        ) + (invalid_file, )
        obj = SubPluginZipFile('', self.plugin)
        obj.find_base_info()
        obj.validate_base_file_in_zip()
        with self.assertRaises(ValidationError) as context:
            obj.validate_file_paths()

        self.assertEqual(
            first=len(context.exception.message_dict),
            second=1,
        )
        self.assertIn(
            member='zip_file',
            container=context.exception.message_dict,
        )
        self.assertEqual(
            first=len(context.exception.message_dict['zip_file']),
            second=1,
        )
        self.assertEqual(
            first=context.exception.message_dict['zip_file'][0],
            second=f'Invalid paths found in zip: {invalid_file}',
        )

        invalid_file = f'invalid/{sub_plugin_basename}/{sub_plugin_basename}.py'
        self.mock_get_file_list.return_value = self._get_file_list(
            sub_plugin_basename=sub_plugin_basename,
        ) + (invalid_file, )
        obj = SubPluginZipFile('', self.plugin)
        obj.find_base_info()
        obj.validate_base_file_in_zip()
        with self.assertRaises(ValidationError) as context:
            obj.validate_file_paths()

        self.assertEqual(
            first=len(context.exception.message_dict),
            second=1,
        )
        self.assertIn(
            member='zip_file',
            container=context.exception.message_dict,
        )
        self.assertEqual(
            first=len(context.exception.message_dict['zip_file']),
            second=1,
        )
        self.assertEqual(
            first=context.exception.message_dict['zip_file'][0],
            second=f'Invalid paths found in zip: {invalid_file}',
        )

    @mock.patch(
        target='project_manager.sub_plugins.helpers.logger',
    )
    def test_validate_requirements_file_failures(self, mock_logger):
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'sub-plugins' / 'test-plugin'
        file_path = base_path / 'test-sub-plugin' / 'test-sub-plugin-v1.0.0.zip'
        self.mock_get_file_list.return_value = []
        plugin = PluginFactory(
            basename='test_plugin',
        )
        sub_plugin_path = SubPluginPathFactory(
            plugin=plugin,
            allow_package_using_init=True,
            path='sub_plugins',
        )
        obj = SubPluginZipFile(
            zip_file=file_path,
            plugin=plugin,
        )
        obj.basename = 'invalid'
        obj.paths = {sub_plugin_path}
        obj.validate_requirements()
        mock_logger.debug.assert_called_once_with('No requirement file found.')

        file_path = base_path / 'test-sub-plugin' / 'test-sub-plugin-invalid-v1.0.0.zip'
        self.mock_get_file_list.return_value = [
            'addons/source-python/plugins/test_plugin/sub_plugins/test_sub_plugin/requirements.json',
        ]
        obj = SubPluginZipFile(
            zip_file=file_path,
            plugin=plugin,
        )
        obj.basename = 'test_sub_plugin'
        obj.paths = {sub_plugin_path}
        with self.assertRaises(ValidationError) as context:
            obj.validate_requirements()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={'zip_file': ['Requirements json file cannot be decoded.']},
        )

    @mock.patch(
        target='project_manager.common.helpers.json.loads',
    )
    @mock.patch(
        target='project_manager.common.helpers.ZipFile',
    )
    @mock.patch(
        target='project_manager.sub_plugins.helpers.ZipFile',
    )
    def test_validate_requirements_file_item_failures(self, _, __, mock_json_loads):
        plugin = PluginFactory()
        custom_package_basename = 'test_custom_package'
        custom_package_slug = custom_package_basename.replace('_', '-')
        custom_package = PackageFactory(
            basename=custom_package_basename,
        )
        custom_package_release = PackageReleaseFactory(
            package=custom_package,
            version='1.0.0',
        )
        download_requirement_url = 'http://example.com/some_file.zip'
        download_requirement = DownloadRequirementFactory(
            url=download_requirement_url,
        )
        pypi_requirement_name = 'some-pypi-package'
        pypi_requirement = PyPiRequirementFactory(
            name=pypi_requirement_name,
        )
        vcs_requirement_url = 'git://git.some-project.org/SomeProject.git'
        vcs_requirement = VersionControlRequirementFactory(
            url=vcs_requirement_url,
        )

        mock_json_loads.return_value = []
        obj = SubPluginZipFile('', plugin=plugin)
        sub_plugin_path = SubPluginPathFactory(
            plugin=plugin,
            allow_package_using_init=True,
            path='sub_plugins',
        )
        obj.paths = {sub_plugin_path}
        with self.assertRaises(ValidationError) as context:
            obj.validate_requirements()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={'zip_file': ['Invalid requirements json file.']},
        )

        group_type = 'invalid'
        mock_json_loads.return_value = {
            group_type: {},
        }
        obj = SubPluginZipFile('', plugin=plugin)
        obj.paths = {sub_plugin_path}
        with self.assertRaises(ValidationError) as context:
            obj.validate_requirements()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={
                'zip_file': [
                    f'Invalid group name "{group_type}" found in requirements '
                    f'json file.'
                ],
            },
        )

        group_type = 'custom'
        mock_json_loads.return_value = {
            group_type: {
                'key': 'value',
            },
        }
        obj = SubPluginZipFile('', plugin=plugin)
        obj.paths = {sub_plugin_path}
        with self.assertRaises(ValidationError) as context:
            obj.validate_requirements()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={
                'zip_file': [
                    f'Invalid group values for "{group_type}" found in '
                    f'requirements json file.'
                ],
            },
        )

        group_type = 'custom'
        mock_json_loads.return_value = {
            group_type: [
                'package',
            ],
        }
        obj = SubPluginZipFile('', plugin=plugin)
        obj.paths = {sub_plugin_path}
        with self.assertRaises(ValidationError) as context:
            obj.validate_requirements()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={
                'zip_file': [
                    f'Invalid object found in "{group_type}" listing in '
                    f'requirements json file.'
                ],
            },
        )

        group_type = 'custom'
        mock_json_loads.return_value = {
            group_type: [
                {'key': 'value'},
            ],
        }
        obj = SubPluginZipFile('', plugin=plugin)
        obj.paths = {sub_plugin_path}
        with self.assertRaises(ValidationError) as context:
            obj.validate_requirements()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={
                'zip_file': [
                    'No basename found for object in "custom" listing in '
                    'requirements json file.'
                ],
            },
        )

        group_type = 'custom'
        invalid_basename = 'invalid'
        mock_json_loads.return_value = {
            group_type: [
                {'basename': invalid_basename},
            ],
        }
        obj = SubPluginZipFile('', plugin=plugin)
        obj.paths = {sub_plugin_path}
        with self.assertRaises(ValidationError) as context:
            obj.validate_requirements()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={
                'zip_file': [
                    f'Custom Package "{invalid_basename}" from requirements '
                    f'json file not found.'
                ],
            },
        )

        group_type = 'custom'
        version = '1.0.1'
        mock_json_loads.return_value = {
            group_type: [
                {
                    'basename': custom_package_slug,
                    'version': version,
                },
            ],
        }
        obj = SubPluginZipFile('', plugin=plugin)
        obj.paths = {sub_plugin_path}
        with self.assertRaises(ValidationError) as context:
            obj.validate_requirements()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={
                'zip_file': [
                    f'Custom Package "{custom_package_slug}" version '
                    f'"{version}", from requirements json file, not found.'
                ],
            },
        )

        for group_type, required_field in {
            'download': 'url',
            'pypi': 'name',
            'vcs': 'url',
        }.items():
            mock_json_loads.return_value = {
                group_type: [
                    {
                        'key': 'value',
                    },
                ],
            }
            obj = SubPluginZipFile('', plugin=plugin)
            obj.paths = {sub_plugin_path}
            with self.assertRaises(ValidationError) as context:
                obj.validate_requirements()

            self.assertDictEqual(
                d1=context.exception.message_dict,
                d2={
                    'zip_file': [
                        f'No {required_field} found for object in '
                        f'"{group_type}" listing in requirements json file.'
                    ],
                },
            )

        mock_json_loads.return_value = {
            'custom': [
                {
                    'basename': custom_package_slug,
                    'version': custom_package_release.version,
                },
            ],
            'download': [
                {
                    'url': download_requirement_url,
                }
            ],
            'pypi': [
                {
                    'name': pypi_requirement_name,
                }
            ],
            'vcs': [
                {
                    'url': vcs_requirement_url,
                }
            ],
        }
        obj = SubPluginZipFile('', plugin=plugin)
        obj.paths = {sub_plugin_path}
        obj.validate_requirements()
        self.assertDictEqual(
            d1=obj.requirements,
            d2={
                'custom': [{
                    'package_requirement': custom_package,
                    'version': custom_package_release.version,
                    'optional': False,
                }],
                'download': [{
                    'download_requirement': download_requirement,
                    'optional': False,
                }],
                'pypi': [{
                    'pypi_requirement': pypi_requirement,
                    'version': None,
                    'optional': False,
                }],
                'vcs': [{
                    'vcs_requirement': vcs_requirement,
                    'optional': False,
                }],
            }
        )


class HelperFunctionsTestCase(TestCase):
    def test_handle_sub_plugin_zip_upload(self):
        obj = SubPluginReleaseFactory()
        plugin_slug = obj.sub_plugin.plugin.slug
        slug = obj.sub_plugin.slug
        self.assertEqual(
            first=handle_sub_plugin_zip_upload(obj),
            second=(
                f'{SUB_PLUGIN_RELEASE_URL}{plugin_slug}/{slug}/'
                f'{slug}-v{obj.version}.zip'
            ),
        )

    def test_handle_sub_plugin_logo_upload(self):
        obj = SubPluginFactory()
        plugin_slug = obj.plugin.slug
        extension = 'jpg'
        filename = f'test_image.{extension}'
        self.assertEqual(
            first=handle_sub_plugin_logo_upload(
                instance=obj,
                filename=filename,
            ),
            second=(
                f'{SUB_PLUGIN_LOGO_URL}{plugin_slug}/{obj.slug}.{extension}'
            ),
        )

    def test_handle_sub_plugin_image_upload(self):
        obj = SubPluginImageFactory()
        plugin_slug = obj.sub_plugin.plugin.slug
        slug = obj.sub_plugin.slug
        extension = 'jpg'
        filename = f'test_image.{extension}'
        image_number = f'{randint(1, 10):04}'
        with mock.patch(
            target='project_manager.sub_plugins.helpers.find_image_number',
            return_value=image_number,
        ):
            self.assertEqual(
                first=handle_sub_plugin_image_upload(
                    instance=obj,
                    filename=filename,
                ),
                second=(
                    f'{SUB_PLUGIN_IMAGE_URL}{plugin_slug}/{slug}/'
                    f'{image_number}.{extension}'
                ),
            )
