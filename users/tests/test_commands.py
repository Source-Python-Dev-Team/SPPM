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
from test_utils.factories.users import AdminUserFactory, ForumUserFactory
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
@override_settings(LOCAL=True)
class CommandsTestCase(TestCase):

    @mock.patch(
        'users.management.commands.associate_super_user.logger',
    )
    def test_associate_super_user(self, mock_logger):
        user = AdminUserFactory()
        self.assertEqual(
            first=ForumUser.objects.count(),
            second=0,
        )
        forum_id = randint(1, 10)
        call_command('associate_super_user', user.username, forum_id)
        self.assertEqual(
            first=ForumUser.objects.count(),
            second=1,
        )
        forum_user = ForumUser.objects.get()
        self.assertEqual(
            first=forum_user.user.id,
            second=user.id,
        )
        self.assertEqual(
            first=forum_user.forum_id,
            second=forum_id,
        )
        mock_logger.info.assert_called_once_with(
            f'User "{user.username}" successfully associated with forum id "{forum_id}".'
        )

    @override_settings(LOCAL=False)
    def test_associate_super_user_local_only(self):
        user = AdminUserFactory()
        self.assertEqual(
            first=ForumUser.objects.count(),
            second=0,
        )
        forum_id = randint(1, 10)
        with self.assertRaises(CommandError) as context:
            call_command('associate_super_user', user.username, forum_id)

        self.assertEqual(
            first=str(context.exception),
            second='Command can only be run for local development.',
        )

    def test_associate_super_user_invalid_username(self):
        user = AdminUserFactory()
        self.assertEqual(
            first=ForumUser.objects.count(),
            second=0,
        )
        forum_id = randint(1, 10)
        username = user.username + '1'
        with self.assertRaises(CommandError) as context:
            call_command('associate_super_user', username, forum_id)

        self.assertEqual(
            first=str(context.exception),
            second=f'User with the username "{username}" was not found.',
        )

    def test_associate_super_user_forum_user_exists(self):
        forum_id = randint(1, 10)
        user = ForumUserFactory(
            forum_id=forum_id,
        )
        with self.assertRaises(CommandError) as context:
            call_command('associate_super_user', user.user.username, forum_id)

        self.assertEqual(
            first=str(context.exception),
            second=(
                f'A user is already associated with the forum id "{forum_id}".'
            ),
        )

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
            f'Successfully created "{count}" users.'
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

    @mock.patch(
        'users.management.commands.create_test_user.logger',
    )
    def test_create_test_user(self, mock_logger):
        username = 'test-user'
        forum_id = randint(1, 10)
        call_command('create_test_user', username, 'password', forum_id)
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
            f'Successfully created user "{username}" and associated it with forum id "{forum_id}".'
        )

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
