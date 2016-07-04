# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db import IntegrityError
from django.test import TestCase

# App
from plugin_manager.users.models import ForumUser


# =============================================================================
# >> TESTS
# =============================================================================
class TestForumUser(TestCase):
    def setUp(self):
        ForumUser.objects.create(username='test_user', id=1)

    def test_username_must_be_unique(self):
        self.assertRaises(
            IntegrityError,
            ForumUser.objects.create,
            username='test_user',
            id=2,
        )

    def test_id_must_be_unique(self):
        self.assertRaises(
            IntegrityError,
            ForumUser.objects.create,
            username='test_user2',
            id=1,
        )
