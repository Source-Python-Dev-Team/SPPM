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
from project_manager.helpers import ProjectZipFile
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
from test_utils.factories.requirements import PyPiRequirementFactory, DownloadRequirementFactory, \
    VersionControlRequirementFactory


class PackageZipFileTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.mock_get_file_list = mock.patch(
            target='project_manager.helpers.ProjectZipFile.get_file_list',
        ).start()
        self.mock_zipfile = mock.patch(
            target='project_manager.helpers.ZipFile',
        )
        self.mock_zipfile.start()

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

    @mock.patch(
        target='project_manager.helpers.logger',
    )
    def test_validate_requirements_file_failures(self, mock_logger):
        self.mock_zipfile.stop()
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'packages'
        file_path = base_path / 'test-package' / 'test-package-v1.0.0.zip'
        self.mock_get_file_list.return_value = []
        obj = PackageZipFile(zip_file=file_path)
        obj.basename = 'invalid'
        obj.validate_requirements()
        mock_logger.debug.assert_called_once_with('No requirement file found.')

        file_path = base_path / 'test-package' / 'test-package-invalid-v1.0.0.zip'
        self.mock_get_file_list.return_value = [
            'addons/source-python/packages/custom/test_package/test_package_requirements.json',
        ]
        obj = PackageZipFile(zip_file=file_path)
        obj.basename = 'test_package'
        with self.assertRaises(ValidationError) as context:
            obj.validate_requirements()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={'zip_file': ['Requirements json file cannot be decoded.']},
        )

    @mock.patch(
        target='project_manager.helpers.json.loads',
    )
    def test_validate_requirements_file_item_failures(self, mock_json_loads):
        custom_package_basename = 'test_custom_package'
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
        obj = PackageZipFile('')
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
        obj = PackageZipFile('')
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
        obj = PackageZipFile('')
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
        obj = PackageZipFile('')
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
        obj = PackageZipFile('')
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
        obj = PackageZipFile('')
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
                    'basename': custom_package_basename,
                    'version': version,
                },
            ],
        }
        obj = PackageZipFile('')
        with self.assertRaises(ValidationError) as context:
            obj.validate_requirements()

        self.assertDictEqual(
            d1=context.exception.message_dict,
            d2={
                'zip_file': [
                    f'Custom Package "{custom_package_basename}" version '
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
            obj = PackageZipFile('')
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
                    'basename': custom_package_basename,
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
        obj = PackageZipFile('')
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
