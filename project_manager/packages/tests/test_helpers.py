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
from project_manager.packages.constants import (
    PACKAGE_ALLOWED_FILE_TYPES,
    PACKAGE_IMAGE_URL,
    PACKAGE_LOGO_URL,
    PACKAGE_PATH,
    PACKAGE_RELEASE_URL,
)
from project_manager.packages.helpers import (
    PackageZipFile,
    handle_package_image_upload,
    handle_package_logo_upload,
    handle_package_zip_upload,
)
from test_utils.factories.packages import (
    PackageFactory,
    PackageImageFactory,
    PackageReleaseFactory,
)


# =============================================================================
# TEST CASES
# =============================================================================
class PackageZipFileTestCase(TestCase):

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
    def _get_module_file_list(package_basename):
        return tuple(
            reversed([
                PACKAGE_PATH.rsplit('/', i)[0] + '/'
                for i in range(1, PACKAGE_PATH.count('/') + 1)
            ])
        ) + (
            f'{PACKAGE_PATH}{package_basename}.py',
            f'{PACKAGE_PATH}{package_basename}_requirements.json',
        )

    @staticmethod
    def _get_package_file_list(package_basename):
        return tuple(
            reversed([
                PACKAGE_PATH.rsplit('/', i)[0] + '/'
                for i in range(1, PACKAGE_PATH.count('/') + 1)
            ])
        ) + (
            f'{PACKAGE_PATH}{package_basename}',
            f'{PACKAGE_PATH}{package_basename}/__init__.py',
            f'{PACKAGE_PATH}{package_basename}/helpers.py',
            f'{PACKAGE_PATH}{package_basename}_requirements.json',
        )

    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(PackageZipFile, ProjectZipFile))

    def test_project_type(self):
        self.assertEqual(
            first=PackageZipFile.project_type,
            second='Package',
        )

    def test_file_types(self):
        self.assertDictEqual(
            d1=PackageZipFile.file_types,
            d2=PACKAGE_ALLOWED_FILE_TYPES,
        )

    def test_find_base_info(self):
        package_basename = 'test_package_as_module'
        self.mock_get_file_list.return_value = self._get_module_file_list(
            package_basename=package_basename,
        )
        obj = PackageZipFile('')
        obj.find_base_info()
        self.assertTrue(expr=obj.is_module)
        self.assertEqual(
            first=obj.basename,
            second=package_basename,
        )

        package_basename = 'test_package_as_package'
        self.mock_get_file_list.return_value = self._get_package_file_list(
            package_basename=package_basename,
        )
        obj = PackageZipFile('')
        obj.find_base_info()
        self.assertFalse(expr=obj.is_module)
        self.assertEqual(
            first=obj.basename,
            second=package_basename,
        )

        self.mock_get_file_list.return_value += (
            f'{PACKAGE_PATH}second_basename/__init__.py',
        )
        with self.assertRaises(ValidationError) as context:
            obj = PackageZipFile('')
            obj.find_base_info()

        self.assertEqual(
            first=context.exception.message,
            second='Multiple base directories found for package.',
        )
        self.assertEqual(
            first=context.exception.code,
            second='multiple',
        )

    def test_get_base_paths(self):
        package_basename = 'test_package_as_module'
        self.mock_get_file_list.return_value = self._get_module_file_list(
            package_basename=package_basename,
        )
        obj = PackageZipFile('')
        obj.find_base_info()
        self.assertListEqual(
            list1=obj.get_base_paths(),
            list2=[f'{PACKAGE_PATH}{package_basename}.py'],
        )

        package_basename = 'test_package_as_package'
        self.mock_get_file_list.return_value = self._get_package_file_list(
            package_basename=package_basename,
        )
        obj = PackageZipFile('')
        obj.find_base_info()
        self.assertListEqual(
            list1=obj.get_base_paths(),
            list2=[
               f'{PACKAGE_PATH}{package_basename}/{package_basename}.py',
               f'{PACKAGE_PATH}{package_basename}/__init__.py',
            ],
        )

    def test_validate_base_file_in_zip(self):
        package_basename = 'test_package_as_module'
        self.mock_get_file_list.return_value = self._get_module_file_list(
            package_basename=package_basename,
        )
        obj = PackageZipFile('')
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
        package_basename = 'test_package_as_module'
        self.mock_get_file_list.return_value = self._get_module_file_list(
            package_basename=package_basename,
        )
        obj = PackageZipFile('')
        obj.find_base_info()
        self.assertEqual(
            first=obj.get_requirement_path(),
            second=f'{PACKAGE_PATH}{package_basename}_requirements.json',
        )

        package_basename = 'test_package_as_package'
        self.mock_get_file_list.return_value = self._get_package_file_list(
            package_basename=package_basename,
        )
        obj = PackageZipFile('')
        obj.find_base_info()
        self.assertEqual(
            first=obj.get_requirement_path(),
            second=f'{PACKAGE_PATH}{package_basename}/requirements.json',
        )

    def test_validate_file_paths(self):
        package_basename = 'test_package_as_module'
        self.mock_get_file_list.return_value = self._get_module_file_list(
            package_basename=package_basename,
        )
        obj = PackageZipFile('')
        obj.find_base_info()
        obj.validate_base_file_in_zip()
        obj.validate_file_paths()

        invalid_file = f'{PACKAGE_PATH}{package_basename}.invalid'
        self.mock_get_file_list.return_value = self._get_module_file_list(
            package_basename=package_basename,
        ) + (invalid_file, )
        obj = PackageZipFile('')
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

        invalid_file = f'invalid/{package_basename}.py'
        self.mock_get_file_list.return_value = self._get_module_file_list(
            package_basename=package_basename,
        ) + (invalid_file, )
        obj = PackageZipFile('')
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
    def test_handle_package_zip_upload(self):
        obj = PackageReleaseFactory()
        slug = obj.package.slug
        self.assertEqual(
            first=handle_package_zip_upload(obj),
            second=f'{PACKAGE_RELEASE_URL}{slug}/{slug}-v{obj.version}.zip'
        )

    def test_handle_package_logo_upload(self):
        obj = PackageFactory()
        extension = 'jpg'
        filename = f'test_image.{extension}'
        self.assertEqual(
            first=handle_package_logo_upload(
                instance=obj,
                filename=filename,
            ),
            second=f'{PACKAGE_LOGO_URL}{obj.slug}.{extension}',
        )

    def test_handle_package_image_upload(self):
        obj = PackageImageFactory()
        slug = obj.package.slug
        extension = 'jpg'
        filename = f'test_image.{extension}'
        image_number = f'{randint(1, 10):04}'
        with mock.patch(
            target='project_manager.packages.helpers.find_image_number',
            return_value=image_number,
        ):
            self.assertEqual(
                first=handle_package_image_upload(
                    instance=obj,
                    filename=filename,
                ),
                second=f'{PACKAGE_IMAGE_URL}{slug}/{image_number}.{extension}',
            )
