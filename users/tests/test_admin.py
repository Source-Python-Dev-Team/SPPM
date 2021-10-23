# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin
from django.test import TestCase

# App
from test_utils.factories.users import ForumUserFactory
from users.admin import ForumUserAdmin, UserAdmin
from users.models import ForumUser, User


# =============================================================================
# TEST CASES
# =============================================================================
class ForumUserAdminTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ForumUserAdmin, admin.ModelAdmin),
        )

    def test_actions(self):
        self.assertIsNone(obj=ForumUserAdmin.actions)

    def test_list_display(self):
        self.assertTupleEqual(
            tuple1=ForumUserAdmin.list_display,
            tuple2=(
                'get_username',
                'forum_id',
            ),
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=ForumUserAdmin.readonly_fields,
            tuple2=(
                'user',
                'forum_id',
            ),
        )

    def test_search_fields(self):
        self.assertTupleEqual(
            tuple1=ForumUserAdmin.search_fields,
            tuple2=('user__username',),
        )

    def test_get_username(self):
        user = ForumUserFactory()
        method = ForumUserAdmin(ForumUser, '').get_username
        self.assertEqual(
            first=method(user),
            second=user.user.username,
        )
        self.assertEqual(
            first=getattr(method, 'short_description'),
            second='Username',
        )
        self.assertEqual(
            first=getattr(method, 'admin_order_field'),
            second='user__username',
        )

    def test_has_add_permission(self):
        self.assertFalse(
            expr=ForumUserAdmin(ForumUser, '').has_add_permission(''),
        )

    def test_has_delete_permission(self):
        self.assertFalse(
            expr=ForumUserAdmin(ForumUser, '').has_delete_permission(''),
        )


class UserAdminTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(UserAdmin, admin.ModelAdmin),
        )

    def test_actions(self):
        self.assertIsNone(obj=UserAdmin.actions)

    def test_fields(self):
        self.assertTupleEqual(
            tuple1=UserAdmin.fields,
            tuple2=(
                'username',
                'is_superuser',
                'is_staff',
            ),
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=UserAdmin.readonly_fields,
            tuple2=('username',),
        )

    def test_has_add_permission(self):
        self.assertFalse(
            expr=UserAdmin(User, '').has_add_permission(''),
        )

    def test_has_delete_permission(self):
        self.assertFalse(
            expr=UserAdmin(User, '').has_delete_permission(''),
        )
