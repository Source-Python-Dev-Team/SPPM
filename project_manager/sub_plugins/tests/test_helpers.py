# =============================================================================
# IMPORTS
# =============================================================================
# Python
from random import randint
from unittest import mock

# Django
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
from test_utils.factories.plugins import PluginFactory, SubPluginPathFactory
from test_utils.factories.sub_plugins import (
    SubPluginFactory,
    SubPluginImageFactory,
    SubPluginReleaseFactory,
)


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginZipFileTestCase(TestCase):
    # TODO: Add tests for SubPluginZipFile class

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
        mock.patch(
            target='project_manager.common.helpers.ZipFile',
        ).start()
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

    def test_find_base_info(self):
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

    def test_validate_base_file_in_zip(self):
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

    def test_get_requirement_path(self):
        sub_plugin_basename = 'test_sub_plugin'
        self.mock_get_file_list.return_value = self._get_file_list(
            sub_plugin_basename=sub_plugin_basename,
        )
        obj = SubPluginZipFile('', self.plugin)
        obj.find_base_info()
        obj.validate_base_file_in_zip()
        self.assertEqual(
            first=obj.get_requirement_path(),
            second=f'{PLUGIN_PATH}{self.plugin.basename}/{sub_plugin_basename}/requirements.json',
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
        self.assertEqual(
            first=obj.get_requirement_path(),
            second=f'{PLUGIN_PATH}{self.plugin.basename}/{sub_plugin_basename}_requirements.json',
        )

    def test_validate_file_paths(self):
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
