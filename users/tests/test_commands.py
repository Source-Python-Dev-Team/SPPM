# =============================================================================
# IMPORTS
# =============================================================================
# Python
from random import randint
from unittest import mock

# Django
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

# App
from test_utils.factories.users import ForumUserFactory
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
@override_settings(LOCAL=True)
class CommandsTestCase(TestCase):

    @mock.patch(
        'users.management.commands.create_random_users.logger',
    )
    def test_create_random_users(self, mock_logger):
        count = randint(1, 10)
        forum_id = randint(1, 10)
        ForumUserFactory(
            forum_id=forum_id,
        )
        call_command('create_random_users', count)
        self.assertEqual(
            first=ForumUser.objects.count(),
            second=count + 1,
        )
        query = ForumUser.objects.values_list('forum_id', flat=True)
        id_list = list(range(1, count + 1))
        id_list.append(count + 1 if forum_id in id_list else forum_id)
        self.assertListEqual(
            list1=list(query.order_by('forum_id')),
            list2=id_list,
        )
        mock_logger.info.assert_called_once_with(
            'Successfully created "%s" users.',
            count,
        )

    @override_settings(LOCAL=False)
    def test_create_random_users_local_only(self):
        forum_id = randint(1, 10)
        ForumUserFactory(
            forum_id=forum_id,
        )
        with self.assertRaises(CommandError) as context:
            call_command('create_random_users', 10)

        self.assertEqual(
            first=str(context.exception),
            second='Command can only be run for local development.',
        )

    def _validate_user_created(self, username, forum_id, mock_logger):
        self.assertEqual(
            first=ForumUser.objects.count(),
            second=1,
        )
        user = ForumUser.objects.get()
        self.assertEqual(
            first=user.forum_id,
            second=forum_id,
        )
        self.assertEqual(
            first=user.user.username,
            second=username,
        )
        mock_logger.info.assert_called_once_with(
            'Successfully created user "%s" and associated it with forum id "%s".',
            username,
            forum_id,
        )
        return user

    @mock.patch(
        'users.management.commands.create_test_user.logger',
    )
    def test_create_test_user(self, mock_logger):
        username = 'test-user'
        forum_id = randint(1, 10)
        call_command('create_test_user', username, 'password', forum_id)
        user = self._validate_user_created(
            username=username,
            forum_id=forum_id,
            mock_logger=mock_logger,
        )
        self.assertFalse(expr=user.user.is_staff)
        self.assertFalse(expr=user.user.is_superuser)

    @mock.patch(
        'users.management.commands.create_test_user.logger',
    )
    def test_create_test_user_is_staff(self, mock_logger):
        username = 'test-user'
        forum_id = randint(1, 10)
        call_command(
            'create_test_user',
            username,
            'password',
            forum_id,
            '--is_staff',
        )
        user = self._validate_user_created(
            username=username,
            forum_id=forum_id,
            mock_logger=mock_logger,
        )
        self.assertTrue(expr=user.user.is_staff)
        self.assertFalse(expr=user.user.is_superuser)

    @mock.patch(
        'users.management.commands.create_test_user.logger',
    )
    def test_create_test_user_is_superuser(self, mock_logger):
        username = 'test-user'
        forum_id = randint(1, 10)
        call_command(
            'create_test_user',
            username,
            'password',
            forum_id,
            '--is_superuser',
        )
        user = self._validate_user_created(
            username=username,
            forum_id=forum_id,
            mock_logger=mock_logger,
        )
        self.assertFalse(expr=user.user.is_staff)
        self.assertTrue(expr=user.user.is_superuser)

    @mock.patch(
        'users.management.commands.create_test_user.logger',
    )
    def test_create_test_user_is_staff_and_superuser(self, mock_logger):
        username = 'test-user'
        forum_id = randint(1, 10)
        call_command(
            'create_test_user',
            username,
            'password',
            forum_id,
            '--is_staff',
            '--is_superuser',
        )
        user = self._validate_user_created(
            username=username,
            forum_id=forum_id,
            mock_logger=mock_logger,
        )
        self.assertTrue(expr=user.user.is_staff)
        self.assertTrue(expr=user.user.is_superuser)

    @override_settings(LOCAL=False)
    def test_create_test_user_local_only(self):
        username = 'test-user'
        forum_id = randint(1, 10)
        with self.assertRaises(CommandError) as context:
            call_command('create_test_user', username, 'password', forum_id)

        self.assertEqual(
            first=str(context.exception),
            second='Command can only be run for local development.',
        )

    def test_create_test_user_username_exists(self):
        forum_id = randint(1, 10)
        user = ForumUserFactory(
            forum_id=forum_id + 1,
        )
        username = user.user.username
        with self.assertRaises(CommandError) as context:
            call_command('create_test_user', username, 'password', forum_id)

        self.assertEqual(
            first=str(context.exception),
            second=f'User with the username "{username}" already exists.',
        )

    def test_create_test_user_forum_id_exists(self):
        forum_id = randint(1, 10)
        user = ForumUserFactory(
            forum_id=forum_id,
        )
        username = user.user.username + '1'
        with self.assertRaises(CommandError) as context:
            call_command('create_test_user', username, 'password', forum_id)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'A user is already associated with the forum id "{forum_id}".'
            ),
        )

    @mock.patch(
        target='users.management.commands.create_test_user.User',
    )
    def test_create_test_user_error_on_create(self, mock_get_user_model):
        manager = mock_get_user_model.objects
        manager.filter.return_value.exists.return_value = False
        message = 'something went wrong'
        manager.create_user.side_effect = ValueError(message)
        username = 'test-user'
        forum_id = randint(1, 10)
        with self.assertRaises(CommandError) as context:
            call_command('create_test_user', username, 'password', forum_id)

        self.assertEqual(
            first=str(context.exception),
            second=f'Unable to create User due to: {message}',
        )
