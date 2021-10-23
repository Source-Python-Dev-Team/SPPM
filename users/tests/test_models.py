# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.db import models
from django.test import TestCase

# App
from test_utils.factories.users import ForumUserFactory, NonAdminUserFactory
from users.constants import (
    FORUM_MEMBER_URL,
    USER_EMAIL_MAX_LENGTH,
    USER_USERNAME_MAX_LENGTH,
)
from users.models import ForumUser, User


# =============================================================================
# GLOBALS
# =============================================================================
UserModel = get_user_model()


# =============================================================================
# TEST CASES
# =============================================================================
class ForumUserTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(ForumUser, models.Model),
        )

    def test_user_field(self):
        field = ForumUser._meta.get_field('user')
        self.assertIsInstance(
            obj=field,
            cls=models.OneToOneField,
        )
        self.assertEqual(
            first=field.remote_field.model,
            second=UserModel,
        )
        self.assertEqual(
            first=field.remote_field.on_delete,
            second=models.CASCADE,
        )
        self.assertEqual(
            first=field.remote_field.related_name,
            second='forum_user',
        )
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_forum_id_field(self):
        field = ForumUser._meta.get_field('forum_id')
        self.assertIsInstance(
            obj=field,
            cls=models.IntegerField,
        )
        self.assertTrue(expr=field.unique)
        self.assertTrue(expr=field.primary_key)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_meta_class(self):
        self.assertEqual(
            first=ForumUser._meta.verbose_name,
            second='Forum User',
        )
        self.assertEqual(
            first=ForumUser._meta.verbose_name_plural,
            second='Forum Users',
        )

    def test__str__(self):
        user = ForumUserFactory()
        self.assertEqual(
            first=str(user),
            second=user.user.username,
        )

    def test_get_forum_url(self):
        user = ForumUserFactory()
        self.assertEqual(
            first=user.get_forum_url(),
            second=FORUM_MEMBER_URL.format(user_id=user.forum_id)
        )


class UserTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(User, AbstractBaseUser),
        )
        self.assertTrue(
            expr=issubclass(User, PermissionsMixin),
        )

    def test_username_field(self):
        field = User._meta.get_field('username')
        self.assertIsInstance(
            obj=field,
            cls=models.CharField,
        )
        self.assertEqual(
            first=field.max_length,
            second=USER_USERNAME_MAX_LENGTH,
        )
        self.assertTrue(expr=field.unique)
        self.assertFalse(expr=field.editable)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_email_field(self):
        field = User._meta.get_field('email')
        self.assertIsInstance(
            obj=field,
            cls=models.EmailField,
        )
        self.assertEqual(
            first=field.max_length,
            second=USER_EMAIL_MAX_LENGTH,
        )
        self.assertTrue(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_is_staff_field(self):
        field = User._meta.get_field('is_staff')
        self.assertIsInstance(
            obj=field,
            cls=models.BooleanField,
        )
        self.assertFalse(expr=field.default)
        self.assertFalse(expr=field.blank)
        self.assertFalse(expr=field.null)

    def test_objects(self):
        self.assertIsInstance(
            obj=User.objects,
            cls=UserManager,
        )

    def test_get_short_name(self):
        user = NonAdminUserFactory()
        self.assertEqual(
            first=user.get_short_name(),
            second=user.username,
        )

    def test_get_full_name(self):
        user = NonAdminUserFactory()
        self.assertEqual(
            first=user.get_full_name(),
            second=user.username,
        )
