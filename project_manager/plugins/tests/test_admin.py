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
from project_manager.plugins.admin import PluginAdmin, PluginReleaseAdmin
from project_manager.plugins.admin.inlines import (
    PluginContributorInline,
    PluginGameInline,
    PluginImageInline,
    PluginTagInline,
    SubPluginPathInline,
)
from project_manager.plugins.models import (
    Plugin,
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginRelease,
    PluginTag,
    SubPluginPath,
)


# =============================================================================
# TEST CASES
# =============================================================================
class PluginAdminTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginAdmin, ProjectAdmin),
        )

    def test_inlines(self):
        self.assertTupleEqual(
            tuple1=PluginAdmin.inlines,
            tuple2=(
                PluginContributorInline,
                PluginGameInline,
                PluginImageInline,
                PluginTagInline,
                SubPluginPathInline,
            ),
        )

    def test_get_queryset(self):
        request = mock.Mock()
        query = PluginAdmin(
            Plugin,
            admin.AdminSite(),
        ).get_queryset(
            request=request,
        ).query
        self.assertDictEqual(
            d1=query.select_related,
            d2={'owner': {'user': {}}}
        )


class TestPluginReleaseAdminTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginReleaseAdmin, ProjectReleaseAdmin),
        )

    def test_fieldsets(self):
        self.assertTupleEqual(
            tuple1=PluginReleaseAdmin.fieldsets,
            tuple2=(
                (
                    'Release Info',
                    {
                        'classes': ('wide',),
                        'fields': (
                            'version',
                            'notes',
                            'zip_file',
                            'plugin',
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
            tuple1=PluginReleaseAdmin.list_display,
            tuple2=(
                'version',
                'created',
                'plugin',
            )
        )

    def test_ordering(self):
        self.assertTupleEqual(
            tuple1=PluginReleaseAdmin.ordering,
            tuple2=(
                'plugin',
                '-created',
            )
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=PluginReleaseAdmin.readonly_fields,
            tuple2=(
                'zip_file',
                'download_count',
                'created',
                'created_by',
                'plugin',
            )
        )

    def test_search_fields(self):
        self.assertTupleEqual(
            tuple1=PluginReleaseAdmin.search_fields,
            tuple2=(
                'version',
                'plugin__name',
            )
        )

    def test_get_queryset(self):
        request = mock.Mock()
        query = PluginReleaseAdmin(
            PluginRelease,
            admin.AdminSite(),
        ).get_queryset(
            request=request,
        ).query
        self.assertDictEqual(
            d1=query.select_related,
            d2={'created_by': {'user': {}}, 'plugin': {}},
        )

    def test_has_add_permission(self):
        obj = PluginReleaseAdmin(PluginRelease, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )

    def test_has_delete_permission(self):
        obj = PluginReleaseAdmin(PluginRelease, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_delete_permission(''),
        )


class PluginContributorInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginContributorInline,
                ProjectContributorInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=PluginContributorInline.model,
            second=PluginContributor,
        )


class PluginGameInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginGameInline,
                ProjectGameInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=PluginGameInline.model,
            second=PluginGame,
        )

    def test_get_queryset(self):
        request = mock.Mock()
        query = PluginGameInline(
            PluginGame,
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
        obj = PluginGameInline(PluginGame, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )


class PluginImageInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginImageInline,
                ProjectImageInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=PluginImageInline.model,
            second=PluginImage,
        )

    def test_has_add_permission(self):
        obj = PluginImageInline(PluginImage, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )


class PluginTagInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginTagInline,
                ProjectTagInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=PluginTagInline.model,
            second=PluginTag,
        )

    def test_get_queryset(self):
        request = mock.Mock()
        query = PluginTagInline(
            PluginTag,
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
        obj = PluginTagInline(PluginTag, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )


class SubPluginPathInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginPathInline,
                admin.StackedInline,
            ),
        )

    def test_extra(self):
        self.assertEqual(
            first=SubPluginPathInline.extra,
            second=0,
        )

    def test_view_on_site(self):
        self.assertFalse(expr=SubPluginPathInline.view_on_site)

    def test_fields(self):
        self.assertTupleEqual(
            tuple1=SubPluginPathInline.fields,
            tuple2=(
                'path',
                'allow_module',
                'allow_package_using_basename',
                'allow_package_using_init',
            ),
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=SubPluginPathInline.readonly_fields,
            tuple2=(),
        )

    def test_model(self):
        self.assertEqual(
            first=SubPluginPathInline.model,
            second=SubPluginPath,
        )

    def test_has_add_permission(self):
        obj = SubPluginPathInline(SubPluginPath, admin.AdminSite())
        self.assertFalse(expr=obj.has_add_permission(''))
