# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
from django.contrib import admin
from django.test import TestCase

# App
from project_manager.common.admin import ProjectAdmin, ProjectReleaseAdmin
from project_manager.common.admin.inlines import (
    ProjectContributorInline,
    ProjectGameInline,
    ProjectImageInline,
    ProjectTagInline,
)
from project_manager.packages.admin import PackageAdmin, PackageReleaseAdmin
from project_manager.packages.admin.inlines import (
    PackageContributorInline,
    PackageGameInline,
    PackageImageInline,
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
            ),
        )


class TestPackageReleaseAdminTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageReleaseAdmin, ProjectReleaseAdmin),
        )

    def test_fieldsets(self):
        self.assertTupleEqual(
            tuple1=PackageReleaseAdmin.fieldsets,
            tuple2=(
                (
                    'Release Info',
                    {
                        'classes': ('wide',),
                        'fields': (
                            'version',
                            'notes',
                            'zip_file',
                            'package',
                        ),
                    }
                ),
                (
                    'Metadata',
                    {
                        'classes': ('collapse',),
                        'fields': (
                            'created',
                            'created_by',
                            'download_count',
                        ),
                    },
                )
            )
        )

    def test_list_display(self):
        self.assertTupleEqual(
            tuple1=PackageReleaseAdmin.list_display,
            tuple2=(
                'version',
                'created',
                'package',
            )
        )

    def test_ordering(self):
        self.assertTupleEqual(
            tuple1=PackageReleaseAdmin.ordering,
            tuple2=(
                'package',
                '-created',
            )
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=PackageReleaseAdmin.readonly_fields,
            tuple2=(
                'zip_file',
                'download_count',
                'created',
                'created_by',
                'package',
            )
        )

    def test_search_fields(self):
        self.assertTupleEqual(
            tuple1=PackageReleaseAdmin.search_fields,
            tuple2=(
                'version',
                'package__name',
            )
        )

    def test_has_add_permission(self):
        obj = PackageReleaseAdmin(PackageRelease, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )

    def test_has_delete_permission(self):
        obj = PackageReleaseAdmin(PackageRelease, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_delete_permission(''),
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
