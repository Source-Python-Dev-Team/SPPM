# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

# App
from project_manager.management.commands.create_secret_key_file import ALLOWED_CHARS


# =============================================================================
# TEST CASES
# =============================================================================
class CommandsTestCase(TestCase):

    @mock.patch(
        target='project_manager.management.commands.create_secret_key_file.SECRET_FILE'
    )
    @mock.patch(
        target='project_manager.management.commands.create_secret_key_file.get_random_string'
    )
    def test_create_secret_key_file(self, mock_get_random_string, mock_secret_file):
        length = 50
        mock_secret_file.isfile.return_value = False
        call_command('create_secret_key_file', length)
        mock_secret_file.isfile.assert_called_once_with()
        mock_get_random_string.assert_called_once_with(
            length=length,
            allowed_chars=ALLOWED_CHARS,
        )
        mock_secret_file.open.assert_called_once_with('w')
        open_file = mock_secret_file.open.return_value.__enter__.return_value
        open_file.write.assert_called_once_with(mock_get_random_string.return_value)

    @mock.patch(
        target='project_manager.management.commands.create_secret_key_file.SECRET_FILE'
    )
    def test_create_secret_key_file_key_file_exists(self, mock_secret_file):
        mock_secret_file.isfile.return_value = True
        with self.assertRaises(CommandError) as context:
            call_command('create_secret_key_file', 50)

        self.assertEqual(
            first=str(context.exception),
            second='Secret key file already exists.'
        )
