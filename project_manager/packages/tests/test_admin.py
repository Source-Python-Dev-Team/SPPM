# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
from django.contrib import admin
from django.test import TestCase

# App
from project_manager.admin.base import ProjectAdmin, ProjectReleaseAdmin
from project_manager.admin.inlines import (
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
    Package,
    PackageContributor,
    PackageGame,
    PackageImage,
    PackageRelease,
    PackageTag,
)


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

    def test_get_queryset(self):
        request = mock.Mock()
        query = PackageAdmin(
            Package,
            admin.AdminSite(),
        ).get_queryset(
            request=request,
        ).query
        self.assertDictEqual(
            d1=query.select_related,
            d2={'owner': {'user': {}}}
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

    def test_get_queryset(self):
        request = mock.Mock()
        query = PackageReleaseAdmin(
            PackageRelease,
            admin.AdminSite(),
        ).get_queryset(
            request=request,
        ).query
        self.assertDictEqual(
            d1=query.select_related,
            d2={'created_by': {'user': {}}, 'package': {}},
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

    def test_get_queryset(self):
        request = mock.Mock()
        query = PackageGameInline(
            PackageGame,
            admin.AdminSite(),
        ).get_queryset(
            request=request,
        ).query
        self.assertDictEqual(
            d1=query.select_related,
            d2={'game': {}}
        )
        self.assertTupleEqual(
            tuple1=query.order_by,
            tuple2=('game__name',),
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

    def test_get_queryset(self):
        request = mock.Mock()
        query = PackageTagInline(
            PackageTag,
            admin.AdminSite(),
        ).get_queryset(
            request=request,
        ).query
        self.assertDictEqual(
            d1=query.select_related,
            d2={'tag': {}}
        )
        self.assertTupleEqual(
            tuple1=query.order_by,
            tuple2=('tag__name',),
        )

    def test_has_add_permission(self):
        obj = PackageTagInline(PackageTag, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )
