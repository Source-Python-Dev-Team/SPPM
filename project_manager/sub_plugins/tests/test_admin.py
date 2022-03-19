# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin
from django.test import TestCase

# App
from project_manager.common.admin import ProjectAdmin
from project_manager.common.admin.inlines import (
    ProjectContributorInline,
    ProjectGameInline,
    ProjectImageInline,
    ProjectTagInline,
)
from project_manager.sub_plugins.admin import SubPluginAdmin
from project_manager.sub_plugins.admin.inlines import (
    SubPluginContributorInline,
    SubPluginGameInline,
    SubPluginImageInline,
    SubPluginTagInline,
)
from project_manager.sub_plugins.models import (
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

    def test_has_add_permission(self):
        obj = SubPluginTagInline(SubPluginTag, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )
