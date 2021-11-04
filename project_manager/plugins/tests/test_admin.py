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
    ProjectReleaseInline,
    ProjectTagInline,
)
from project_manager.plugins.admin import PluginAdmin
from project_manager.plugins.admin.inlines import (
    PluginContributorInline,
    PluginGameInline,
    PluginImageInline,
    PluginReleaseInline,
    PluginTagInline,
    SubPluginPathInline,
)
from project_manager.plugins.models import (
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
                PluginReleaseInline,
            ),
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

    def test_has_add_permission(self):
        obj = PluginTagInline(PluginTag, admin.AdminSite())
        self.assertFalse(
            expr=obj.has_add_permission(''),
        )


class PluginReleaseInlineTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleaseInline,
                ProjectReleaseInline,
            ),
        )

    def test_model(self):
        self.assertEqual(
            first=PluginReleaseInline.model,
            second=PluginRelease,
        )

    def test_has_add_permission(self):
        obj = PluginReleaseInline(PluginRelease, admin.AdminSite())
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
            tuple2=('path',),
        )

    def test_model(self):
        self.assertEqual(
            first=SubPluginPathInline.model,
            second=SubPluginPath,
        )

    def test_has_add_permission(self):
        obj = SubPluginPathInline(SubPluginPath, admin.AdminSite())
        self.assertFalse(expr=obj.has_add_permission(''))
