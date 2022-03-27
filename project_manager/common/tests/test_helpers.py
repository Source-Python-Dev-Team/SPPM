# =============================================================================
# IMPORTS
# =============================================================================
# Python
from random import sample
from unittest import mock
from zipfile import BadZipFile

# Django
from django.core.exceptions import ValidationError
from django.test import TestCase

# App
from project_manager.common.constants import (
    CANNOT_BE_NAMED,
    CANNOT_START_WITH,
)
from project_manager.common.helpers import (
    ProjectZipFile,
    find_image_number,
    handle_project_logo_upload,
    handle_release_zip_file_upload,
)


# =============================================================================
# TEST CASES
# =============================================================================
class ProjectZipFileTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.mock_zip_file = mock.patch(
            target='project_manager.common.helpers.ZipFile',
        ).start()

    def tearDown(self) -> None:
        super().tearDown()
        mock.patch.stopall()

    def test_get_file_list(self):
        zip_obj = self.mock_zip_file.return_value.__enter__.return_value
        name_list = zip_obj.namelist.return_value = (
            'addons/',
            'addons/source-python/',
            'addons/source-python/plugins/',
            'addons/source-python/plugins/test_plugin/',
            'addons/source-python/plugins/test_plugin/test_plugin.py',
            'addons/source-python/plugins/test_plugin/requirements.json',
        )
        zip_file = 'test.zip'
        obj = ProjectZipFile(zip_file)
        self.assertEqual(
            first=obj.zip_file,
            second=zip_file,
        )
        self.assertListEqual(
            list1=obj.file_list,
            list2=list(name_list[4:]),
        )

        zip_obj.namelist.side_effect = BadZipFile()
        with self.assertRaises(ValidationError) as context:
            ProjectZipFile(zip_file)

        self.assertEqual(
            first=len(context.exception.message_dict),
            second=1,
        )
        self.assertIn(
            member='zip_file',
            container=context.exception.message_dict,
        )
        errors = context.exception.message_dict['zip_file']
        self.assertEqual(
            first=len(errors),
            second=1,
        )
        self.assertEqual(
            first=errors[0],
            second='Given file is not a valid zip file.',
        )

    def test_project_type_required(self):
        obj = ProjectZipFile('')
        with self.assertRaises(NotImplementedError) as context:
            _ = obj.project_type

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"project_type" attribute.'
            ),
        )

    def test_file_types_required(self):
        obj = ProjectZipFile('')
        with self.assertRaises(NotImplementedError) as context:
            _ = obj.file_types

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"file_types" attribute.'
            ),
        )

    def test_find_base_info_required(self):
        obj = ProjectZipFile('')
        with self.assertRaises(NotImplementedError) as context:
            obj.find_base_info()

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"find_base_info" method.'
            ),
        )

    def test_get_base_paths_required(self):
        obj = ProjectZipFile('')
        with self.assertRaises(NotImplementedError) as context:
            obj.get_base_paths()

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"get_base_paths" method.'
            ),
        )

    def test_get_requirement_path_required(self):
        obj = ProjectZipFile('')
        with self.assertRaises(NotImplementedError) as context:
            obj.get_requirement_path()

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'Class "{obj.__class__.__name__}" must implement a '
                f'"get_requirement_path" method.'
            ),
        )

    def test_validate_basename(self):
        class TestProjectZipFile(ProjectZipFile):
            project_type = 'test'

        obj = TestProjectZipFile('')
        with self.assertRaises(ValidationError) as context:
            obj.validate_basename()

        self.assertEqual(
            first=context.exception.message,
            second=f'No base directory or file found for {obj.project_type}.',
        )
        self.assertEqual(
            first=context.exception.code,
            second='not-found',
        )

        for name in CANNOT_BE_NAMED:
            obj.basename = name
            with self.assertRaises(ValidationError) as context:
                obj.validate_basename()

            self.assertEqual(
                first=context.exception.message,
                second=f'{obj.project_type} basename cannot be "{obj.basename}".',
            )
            self.assertEqual(
                first=context.exception.code,
                second='invalid',
            )

        for prefix in CANNOT_START_WITH:
            obj.basename = f'{prefix}test'
            with self.assertRaises(ValidationError) as context:
                obj.validate_basename()

            self.assertEqual(
                first=context.exception.message,
                second=(
                    f'{obj.project_type} basename cannot start with '
                    f'"{prefix}".'
                ),
            )
            self.assertEqual(
                first=context.exception.code,
                second='invalid',
            )

        obj.basename = 'base_name'
        obj.validate_basename()


class CommonHelperFunctionsTestCase(TestCase):

    @mock.patch(
        target='project_manager.common.models.settings.MEDIA_ROOT',
    )
    def test_find_image_number(self, mock_media_root):
        base_directory = mock_media_root.__truediv__.return_value
        path = base_directory.__truediv__.return_value.__truediv__.return_value
        path.isdir.return_value = False
        self.assertEqual(
            first=find_image_number(
                directory='directory',
                slug='slug',
            ),
            second=f'{1:04}',
        )

        path.isdir.return_value = True
        existing_files = sample(range(11), 4)
        max_value = max(existing_files)
        path.files.return_value = (
            mock.Mock(stem=n)
            for n in existing_files
        )
        self.assertEqual(
            first=find_image_number(
                directory='directory',
                slug='slug',
            ),
            second=f'{max_value + 1:04}',
        )

    @staticmethod
    def test_handle_project_logo_upload():
        obj = mock.Mock()
        filename = 'test.zip'
        handle_project_logo_upload(
            instance=obj,
            filename=filename,
        )
        obj.handle_logo_upload.assert_called_once_with(filename)

    @staticmethod
    def test_handle_release_zip_file_upload():
        obj = mock.Mock()
        filename = 'test.zip'
        handle_release_zip_file_upload(
            instance=obj,
            filename=filename,
        )
        obj.handle_zip_file_upload.assert_called_once_with()
