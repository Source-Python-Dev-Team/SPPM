# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
from django.contrib import admin
from django.test import TestCase

# App
from project_manager.common.admin import ProjectAdmin
from project_manager.common.admin.inlines import (
    ProjectContributorInline,
    ProjectGameInline,
    ProjectImageInline,
    ProjectReleaseInline,
    ProjectTagInline,
)
from project_manager.packages.admin import PackageAdmin
from project_manager.packages.admin.inlines import (
    PackageContributorInline,
    PackageGameInline,
    PackageImageInline,
    PackageReleaseInline,
    PackageTagInline,
)
from project_manager.packages.models import (
    PackageContributor,
    PackageGame,
    PackageImage,
    PackageRelease,
    PackageTag,
)
from test_utils.factories.packages import PackageFactory
from test_utils.factories.users import ForumUserFactory
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class PackageAdminTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageAdmin, ProjectAdmin),
        )

    def test_inlines(self):
        self.assertTupleEqual(
            tuple1=PackageAdmin.inlines,
            tuple2=(
                PackageContributorInline,
                PackageGameInline,
                PackageImageInline,
                PackageTagInline,
                PackageReleaseInline,
            ),
        )


class PackageContributorInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageContributorInline,
                ProjectContributorInline,
            ),
        )

    @mock.patch(
        target='django.contrib.admin.options.InlineModelAdmin.get_formset',
    )
    def test_get_formset(self, mock_super_get_formset):
        user = ForumUserFactory()
        package = PackageFactory()
        field = mock_super_get_formset.return_value.form.base_fields['user']
        field.queryset = ForumUser.objects.all()
        self.assertCountEqual(
            first=list(field.queryset),
            second=[package.owner, user],
        )
        obj = PackageContributorInline(PackageContributor, admin.AdminSite())
        obj.get_formset('', package)
        self.assertListEqual(
            list1=list(field.queryset),
            list2=[user],
        )

    def test_model(self):
        self.assertEqual(
            first=PackageContributorInline.model,
            second=PackageContributor,
        )


class PackageGameInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageGameInline,
                ProjectGameInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=PackageGameInline.model,
            second=PackageGame,
        )

    def test_has_add_permission(self):
        obj = PackageGameInline(PackageGame, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )


class PackageImageInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageImageInline,
                ProjectImageInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=PackageImageInline.model,
            second=PackageImage,
        )

    def test_has_add_permission(self):
        obj = PackageImageInline(PackageImage, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )


class PackageTagInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageTagInline,
                ProjectTagInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=PackageTagInline.model,
            second=PackageTag,
        )

    def test_has_add_permission(self):
        obj = PackageTagInline(PackageTag, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )


class PackageReleaseInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleaseInline,
                ProjectReleaseInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=PackageReleaseInline.model,
            second=PackageRelease,
        )

    def test_get_queryset(self):
        obj = PackageReleaseInline(PackageRelease, admin.AdminSite())
        self.assertTupleEqual(
            tuple1=obj.get_queryset(mock.Mock()).query.order_by,
            tuple2=('-created',),
        )

    def test_has_add_permission(self):
        obj = PackageReleaseInline(PackageRelease, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )
