# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin
from django.test import TestCase

# App
from tags.admin import TagAdmin
from tags.models import Tag


# =============================================================================
# TEST CASES
# =============================================================================
class TagAdminTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(TagAdmin, admin.ModelAdmin),
        )

    def test_actions(self):
        self.assertIsNone(obj=TagAdmin.actions)

    def test_list_display(self):
        self.assertTupleEqual(
            tuple1=TagAdmin.list_display,
            tuple2=(
                'name',
                'black_listed',
                'creator',
            ),
        )

    def test_list_display_links(self):
        self.assertIsNone(obj=TagAdmin.list_display_links)

    def test_list_filter(self):
        self.assertTupleEqual(
            tuple1=TagAdmin.list_filter,
            tuple2=('black_listed',),
        )

    def test_list_editable(self):
        self.assertTupleEqual(
            tuple1=TagAdmin.list_editable,
            tuple2=(
                'black_listed',
                'creator',
            ),
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=TagAdmin.readonly_fields,
            tuple2=('name',),
        )

    def test_has_add_permission(self):
        self.assertFalse(
            expr=TagAdmin(Tag, '').has_add_permission(''),
        )

    def test_has_delete_permission(self):
        self.assertFalse(
            expr=TagAdmin(Tag, '').has_delete_permission(''),
        )
