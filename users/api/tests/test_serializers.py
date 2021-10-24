# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ListSerializer, ModelSerializer

# App
from project_manager.packages.models import Package
from project_manager.plugins.models import Plugin
from project_manager.sub_plugins.models import SubPlugin
from users.api.serializers import (
    ForumUserSerializer,
    PackageContributionSerializer,
    PluginContributionSerializer,
    ProjectContributionSerializer,
    SubPluginContributionSerializer,
)
from users.api.serializers.common import ForumUserContributorSerializer
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class ForumUserSerializerTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ForumUserSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ForumUserSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=7,
        )

        self.assertIn(
            member='username',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['username'],
            cls=SerializerMethodField,
        )

        self.assertIn(
            member='packages',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['packages'],
            cls=ListSerializer,
        )
        self.assertTrue(expr=declared_fields['packages'].many)
        self.assertTrue(expr=declared_fields['packages'].read_only)
        self.assertIsInstance(
            obj=declared_fields['packages'].child,
            cls=PackageContributionSerializer,
        )
        self.assertTrue(expr=declared_fields['packages'].child.read_only)

        self.assertIn(
            member='package_contributions',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['package_contributions'],
            cls=ListSerializer,
        )
        self.assertTrue(expr=declared_fields['package_contributions'].many)
        self.assertTrue(expr=declared_fields['package_contributions'].read_only)
        self.assertIsInstance(
            obj=declared_fields['package_contributions'].child,
            cls=PackageContributionSerializer,
        )
        self.assertTrue(expr=declared_fields['package_contributions'].child.read_only)

        self.assertIn(
            member='plugins',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['plugins'],
            cls=ListSerializer,
        )
        self.assertTrue(expr=declared_fields['plugins'].many)
        self.assertTrue(expr=declared_fields['plugins'].read_only)
        self.assertIsInstance(
            obj=declared_fields['plugins'].child,
            cls=PluginContributionSerializer,
        )
        self.assertTrue(expr=declared_fields['plugins'].child.read_only)

        self.assertIn(
            member='plugin_contributions',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['plugin_contributions'],
            cls=ListSerializer,
        )
        self.assertTrue(expr=declared_fields['plugin_contributions'].many)
        self.assertTrue(expr=declared_fields['plugin_contributions'].read_only)
        self.assertIsInstance(
            obj=declared_fields['plugin_contributions'].child,
            cls=PluginContributionSerializer,
        )
        self.assertTrue(expr=declared_fields['plugin_contributions'].child.read_only)

        self.assertIn(
            member='subplugins',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['subplugins'],
            cls=ListSerializer,
        )
        self.assertTrue(expr=declared_fields['subplugins'].many)
        self.assertTrue(expr=declared_fields['subplugins'].read_only)
        self.assertIsInstance(
            obj=declared_fields['subplugins'].child,
            cls=SubPluginContributionSerializer,
        )
        self.assertTrue(expr=declared_fields['subplugins'].child.read_only)

        self.assertIn(
            member='subplugin_contributions',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['subplugin_contributions'],
            cls=ListSerializer,
        )
        self.assertTrue(expr=declared_fields['subplugin_contributions'].many)
        self.assertTrue(expr=declared_fields['subplugin_contributions'].read_only)
        self.assertIsInstance(
            obj=declared_fields['subplugin_contributions'].child,
            cls=SubPluginContributionSerializer,
        )
        self.assertTrue(expr=declared_fields['subplugin_contributions'].child.read_only)

    def test_meta_class(self):
        self.assertEqual(
            first=ForumUserSerializer.Meta.model,
            second=ForumUser,
        )
        self.assertTupleEqual(
            tuple1=ForumUserSerializer.Meta.fields,
            tuple2=(
                'forum_id',
                'username',
                'packages',
                'package_contributions',
                'plugins',
                'plugin_contributions',
                'subplugins',
                'subplugin_contributions',
            ),
        )


class PackageContributionSerializerTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageContributionSerializer, ProjectContributionSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(PackageContributionSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=0,
        )

    def test_meta_class(self):
        self.assertEqual(
            first=PackageContributionSerializer.Meta.model,
            second=Package,
        )
        self.assertTrue(
            expr=issubclass(
                PackageContributionSerializer.Meta,
                ProjectContributionSerializer.Meta,
            ),
        )
        self.assertTupleEqual(
            tuple1=PackageContributionSerializer.Meta.fields,
            tuple2=ProjectContributionSerializer.Meta.fields,
        )


class PluginContributionSerializerTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginContributionSerializer, ProjectContributionSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(PluginContributionSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=0,
        )

    def test_meta_class(self):
        self.assertEqual(
            first=PluginContributionSerializer.Meta.model,
            second=Plugin,
        )
        self.assertTrue(
            expr=issubclass(
                PluginContributionSerializer.Meta,
                ProjectContributionSerializer.Meta,
            ),
        )
        self.assertTupleEqual(
            tuple1=PluginContributionSerializer.Meta.fields,
            tuple2=ProjectContributionSerializer.Meta.fields,
        )


class ProjectContributionSerializerTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ProjectContributionSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ProjectContributionSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=0,
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ProjectContributionSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
            ),
        )


class SubPluginContributionSerializerTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginContributionSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(SubPluginContributionSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=1,
        )

        self.assertIn(
            member='plugin',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['plugin'],
            cls=PluginContributionSerializer,
        )

    def test_meta_class(self):
        self.assertEqual(
            first=SubPluginContributionSerializer.Meta.model,
            second=SubPlugin,
        )
        self.assertTupleEqual(
            tuple1=SubPluginContributionSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
                'plugin',
            ),
        )


class ForumUserContributorSerializerTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ForumUserContributorSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ForumUserContributorSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=1,
        )

        self.assertIn(
            member='username',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['username'],
            cls=SerializerMethodField,
        )

    def test_meta_class(self):
        self.assertEqual(
            first=ForumUserContributorSerializer.Meta.model,
            second=ForumUser,
        )
        self.assertTupleEqual(
            tuple1=ForumUserContributorSerializer.Meta.fields,
            tuple2=(
                'forum_id',
                'username',
            ),
        )
