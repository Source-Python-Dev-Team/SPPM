# =============================================================================
# IMPORTS
# =============================================================================
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
from project_manager.common.models import Project


# =============================================================================
# TEST CASES
# =============================================================================
class ProjectAdminTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectAdmin, admin.ModelAdmin),
        )

    def test_actions(self):
        self.assertIsNone(obj=ProjectAdmin.actions)

    def test_fieldsets(self):
        self.assertTupleEqual(
            tuple1=ProjectAdmin.fieldsets,
            tuple2=(
                (
                    'Project Info',
                    {
                        'classes': ('wide',),
                        'fields': (
                            'name',
                            'owner',
                            'configuration',
                            'description',
                            'synopsis',
                            'logo',
                            'topic',
                        ),
                    }
                ),
                (
                    'Metadata',
                    {
                        'classes': ('collapse',),
                        'fields': (
                            'basename',
                            'slug',
                            'created',
                            'updated',
                        ),
                    },
                )
            ),
        )

    def test_list_display(self):
        self.assertTupleEqual(
            tuple1=ProjectAdmin.list_display,
            tuple2=(
                'name',
                'basename',
                'owner',
            ),
        )

    def test_raw_id_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectAdmin.raw_id_fields,
            tuple2=('owner',),
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectAdmin.readonly_fields,
            tuple2=(
                'basename',
                'created',
                'slug',
                'updated',
            ),
        )

    def test_search_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectAdmin.search_fields,
            tuple2=(
                'name',
                'basename',
                'owner__user__username',
                'contributors__user__username',
            )
        )

    def test_has_add_permission(self):
        self.assertFalse(
            expr=ProjectAdmin(Project, '').has_add_permission(''),
        )

    def test_has_delete_permission(self):
        self.assertFalse(
            expr=ProjectAdmin(Project, '').has_delete_permission(''),
        )


class ProjectReleaseAdminTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(ProjectReleaseAdmin, admin.ModelAdmin))

    def test_fieldsets(self):
        self.assertTupleEqual(
            tuple1=ProjectReleaseAdmin.fieldsets,
            tuple2=(
                (
                    'Release Info',
                    {
                        'classes': ('wide',),
                        'fields': (
                            'version',
                            'notes',
                            'zip_file',
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
            tuple1=ProjectReleaseAdmin.list_display,
            tuple2=(
                'version',
                'created',
            )
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectReleaseAdmin.readonly_fields,
            tuple2=(
                'zip_file',
                'download_count',
                'created',
                'created_by',
            )
        )

    def test_search_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectReleaseAdmin.search_fields,
            tuple2=(
                'version',
            )
        )

    def test_view_on_site(self):
        self.assertFalse(expr=ProjectReleaseAdmin.view_on_site)


class ProjectContributorInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectContributorInline, admin.TabularInline),
        )

    def test_extra(self):
        self.assertEqual(
            first=ProjectContributorInline.extra,
            second=0,
        )

    def test_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectContributorInline.fields,
            tuple2=('user',),
        )

    def test_raw_id_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectContributorInline.raw_id_fields,
            tuple2=('user',),
        )


class ProjectGameInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectGameInline, admin.TabularInline),
        )

    def test_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectGameInline.fields,
            tuple2=('game',),
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectGameInline.readonly_fields,
            tuple2=('game',),
        )


class ProjectImageInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectImageInline, admin.TabularInline),
        )

    def test_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectImageInline.fields,
            tuple2=(
                'image',
                'created',
            ),
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectImageInline.readonly_fields,
            tuple2=(
                'image',
                'created',
            ),
        )


class ProjectTagInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectTagInline, admin.TabularInline),
        )

    def test_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectTagInline.fields,
            tuple2=('tag',),
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=ProjectTagInline.readonly_fields,
            tuple2=('tag',),
        )
