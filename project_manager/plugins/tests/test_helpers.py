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
from project_manager.plugins.constants import (
    PLUGIN_ALLOWED_FILE_TYPES,
    PLUGIN_IMAGE_URL,
    PLUGIN_LOGO_URL,
    PLUGIN_PATH,
    PLUGIN_RELEASE_URL,
)
from project_manager.plugins.helpers import (
    PluginZipFile,
    handle_plugin_image_upload,
    handle_plugin_logo_upload,
    handle_plugin_zip_upload,
)
from test_utils.factories.plugins import (
    PluginFactory,
    PluginImageFactory,
    PluginReleaseFactory,
)


# =============================================================================
# TEST CASES
# =============================================================================
class PluginZipFileTestCase(TestCase):

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

    @staticmethod
    def _get_file_list(plugin_basename):
        return tuple(
            reversed([
                PLUGIN_PATH.rsplit('/', i)[0] + '/'
                for i in range(1, PLUGIN_PATH.count('/') + 1)
            ])
        ) + (
            f'{PLUGIN_PATH}{plugin_basename}',
            f'{PLUGIN_PATH}{plugin_basename}/__init__.py',
            f'{PLUGIN_PATH}{plugin_basename}/{plugin_basename}.py',
            f'{PLUGIN_PATH}{plugin_basename}/helpers.py',
            f'{PLUGIN_PATH}{plugin_basename}/requirements.json',
        )

    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(PluginZipFile, ProjectZipFile))

    def test_project_type(self):
        self.assertEqual(
            first=PluginZipFile.project_type,
            second='Plugin',
        )

    def test_file_types(self):
        self.assertDictEqual(
            d1=PluginZipFile.file_types,
            d2=PLUGIN_ALLOWED_FILE_TYPES,
        )

    def test_find_base_info(self):
        plugin_basename = 'test_plugin'
        self.mock_get_file_list.return_value = self._get_file_list(
            plugin_basename=plugin_basename,
        )
        obj = PluginZipFile('')
        obj.find_base_info()
        self.assertEqual(
            first=obj.basename,
            second=plugin_basename,
        )

        self.mock_get_file_list.return_value += (
            f'{PLUGIN_PATH}second_basename/__init__.py',
        )
        with self.assertRaises(ValidationError) as context:
            obj = PluginZipFile('')
            obj.find_base_info()

        self.assertEqual(
            first=context.exception.message,
            second='Multiple base directories found for plugin.',
        )
        self.assertEqual(
            first=context.exception.code,
            second='multiple',
        )

    def test_get_base_paths(self):
        plugin_basename = 'test_plugin'
        self.mock_get_file_list.return_value = self._get_file_list(
            plugin_basename=plugin_basename,
        )
        obj = PluginZipFile('')
        obj.find_base_info()
        self.assertListEqual(
            list1=obj.get_base_paths(),
            list2=[f'{PLUGIN_PATH}{plugin_basename}/{plugin_basename}.py'],
        )

    def test_validate_base_file_in_zip(self):
        plugin_basename = 'test_plugin'
        self.mock_get_file_list.return_value = self._get_file_list(
            plugin_basename=plugin_basename,
        )
        obj = PluginZipFile('')
        obj.find_base_info()
        obj.validate_base_file_in_zip()

        obj.basename = 'invalid'
        with self.assertRaises(ValidationError) as context:
            obj.validate_base_file_in_zip()

        self.assertEqual(
            first=context.exception.message,
            second='No primary file found in zip.',
        )
        self.assertEqual(
            first=context.exception.code,
            second='not-found',
        )

    def test_get_requirement_path(self):
        plugin_basename = 'test_plugin'
        self.mock_get_file_list.return_value = self._get_file_list(
            plugin_basename=plugin_basename,
        )
        obj = PluginZipFile('')
        obj.find_base_info()
        self.assertEqual(
            first=obj.get_requirement_path(),
            second=f'{PLUGIN_PATH}{plugin_basename}/requirements.json',
        )

    def test_validate_file_paths(self):
        plugin_basename = 'test_plugin'
        self.mock_get_file_list.return_value = self._get_file_list(
            plugin_basename=plugin_basename,
        )
        obj = PluginZipFile('')
        obj.find_base_info()
        obj.validate_base_file_in_zip()
        obj.validate_file_paths()

        invalid_file = f'{PLUGIN_PATH}{plugin_basename}/{plugin_basename}.invalid'
        self.mock_get_file_list.return_value = self._get_file_list(
            plugin_basename=plugin_basename,
        ) + (invalid_file, )
        obj = PluginZipFile('')
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

        invalid_file = f'invalid/{plugin_basename}/{plugin_basename}.py'
        self.mock_get_file_list.return_value = self._get_file_list(
            plugin_basename=plugin_basename,
        ) + (invalid_file, )
        obj = PluginZipFile('')
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
    def test_handle_plugin_zip_upload(self):
        obj = PluginReleaseFactory()
        slug = obj.plugin.slug
        self.assertEqual(
            first=handle_plugin_zip_upload(obj),
            second=f'{PLUGIN_RELEASE_URL}{slug}/{slug}-v{obj.version}.zip'
        )

    def test_handle_plugin_logo_upload(self):
        obj = PluginFactory()
        extension = 'jpg'
        filename = f'test_image.{extension}'
        self.assertEqual(
            first=handle_plugin_logo_upload(
                instance=obj,
                filename=filename,
            ),
            second=f'{PLUGIN_LOGO_URL}{obj.slug}.{extension}',
        )

    def test_handle_plugin_image_upload(self):
        obj = PluginImageFactory()
        slug = obj.plugin.slug
        extension = 'jpg'
        filename = f'test_image.{extension}'
        image_number = f'{randint(1, 10):04}'
        with mock.patch(
            target='project_manager.plugins.helpers.find_image_number',
            return_value=image_number,
        ):
            self.assertEqual(
                first=handle_plugin_image_upload(
                    instance=obj,
                    filename=filename,
                ),
                second=f'{PLUGIN_IMAGE_URL}{slug}/{image_number}.{extension}',
            )
