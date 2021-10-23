# =============================================================================
# IMPORTS
# =============================================================================
# Python
from random import randint
from unittest import mock

# Django
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

# App
from test_utils.factories.users import AdminUserFactory, ForumUserFactory
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class CommandsTestCase(TestCase):

    def test_associate_super_user(self):
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

    def test_create_random_users(self):
        forum_id = randint(1, 10)
        ForumUserFactory(
            forum_id=forum_id,
        )
        call_command('create_random_users', 10)
        self.assertEqual(
            first=ForumUser.objects.count(),
            second=11,
        )
        query = ForumUser.objects.values_list('forum_id', flat=True)
        self.assertListEqual(
            list1=list(query.order_by('forum_id')),
            list2=list(range(1, 12)),
        )

    def test_create_test_user(self):
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
