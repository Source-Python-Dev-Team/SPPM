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
from project_manager.sub_plugins.admin import (
    SubPluginAdmin,
    SubPluginReleaseAdmin,
)
from project_manager.sub_plugins.admin.inlines import (
    SubPluginContributorInline,
    SubPluginGameInline,
    SubPluginImageInline,
    SubPluginTagInline,
)
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginContributor,
    SubPluginGame,
    SubPluginImage,
    SubPluginRelease,
    SubPluginTag,
)


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginAdminTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginAdmin, ProjectAdmin),
        )

    def test_inlines(self):
        self.assertTupleEqual(
            tuple1=SubPluginAdmin.inlines,
            tuple2=(
                SubPluginContributorInline,
                SubPluginGameInline,
                SubPluginImageInline,
                SubPluginTagInline,
            ),
        )

    def test_get_queryset(self):
        request = mock.Mock()
        query = SubPluginAdmin(
            SubPlugin,
            admin.AdminSite(),
        ).get_queryset(
            request=request,
        ).query
        self.assertDictEqual(
            d1=query.select_related,
            d2={'owner': {'user': {}}, 'plugin': {}},
        )


class TestSubPluginReleaseAdminTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginReleaseAdmin, ProjectReleaseAdmin),
        )

    def test_fieldsets(self):
        self.assertTupleEqual(
            tuple1=SubPluginReleaseAdmin.fieldsets,
            tuple2=(
                (
                    'Release Info',
                    {
                        'classes': ('wide',),
                        'fields': (
                            'version',
                            'notes',
                            'zip_file',
                            'sub_plugin',
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
            tuple1=SubPluginReleaseAdmin.list_display,
            tuple2=(
                'version',
                'created',
                'sub_plugin',
            )
        )

    def test_ordering(self):
        self.assertTupleEqual(
            tuple1=SubPluginReleaseAdmin.ordering,
            tuple2=(
                'sub_plugin',
                '-created',
            )
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=SubPluginReleaseAdmin.readonly_fields,
            tuple2=(
                'zip_file',
                'download_count',
                'created',
                'created_by',
                'sub_plugin',
            )
        )

    def test_search_fields(self):
        self.assertTupleEqual(
            tuple1=SubPluginReleaseAdmin.search_fields,
            tuple2=(
                'version',
                'sub_plugin__name',
            )
        )

    def test_get_queryset(self):
        request = mock.Mock()
        query = SubPluginReleaseAdmin(
            SubPluginRelease,
            admin.AdminSite(),
        ).get_queryset(
            request=request,
        ).query
        self.assertDictEqual(
            d1=query.select_related,
            d2={'created_by': {'user': {}}, 'sub_plugin': {'plugin': {}}},
        )

    def test_has_add_permission(self):
        obj = SubPluginReleaseAdmin(SubPluginRelease, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )

    def test_has_delete_permission(self):
        obj = SubPluginReleaseAdmin(SubPluginRelease, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_delete_permission(''),
        )


class SubPluginContributorInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginContributorInline,
                ProjectContributorInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=SubPluginContributorInline.model,
            second=SubPluginContributor,
        )


class SubPluginGameInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginGameInline,
                ProjectGameInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=SubPluginGameInline.model,
            second=SubPluginGame,
        )

    def test_get_queryset(self):
        request = mock.Mock()
        query = SubPluginGameInline(
            SubPluginGame,
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
        obj = SubPluginGameInline(SubPluginGame, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )


class SubPluginImageInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginImageInline,
                ProjectImageInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=SubPluginImageInline.model,
            second=SubPluginImage,
        )

    def test_has_add_permission(self):
        obj = SubPluginImageInline(SubPluginImage, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )


class SubPluginTagInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginTagInline,
                ProjectTagInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=SubPluginTagInline.model,
            second=SubPluginTag,
        )

    def test_get_queryset(self):
        request = mock.Mock()
        query = SubPluginTagInline(
            SubPluginTag,
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
        obj = SubPluginTagInline(SubPluginTag, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )
