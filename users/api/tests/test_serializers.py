# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase

# Third Party Django
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.serializers import ListSerializer, ModelSerializer

# App
from project_manager.packages.api.common.serializers import MinimalPackageSerializer
from project_manager.plugins.api.common.serializers import MinimalPluginSerializer
from project_manager.sub_plugins.api.common.serializers import MinimalSubPluginSerializer
from users.api.serializers import (
    ForumUserListSerializer,
    ForumUserRetrieveSerializer,
)
from users.api.common.serializers import ForumUserContributorSerializer
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class ForumUserRetrieveSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ForumUserRetrieveSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ForumUserRetrieveSerializer, '_declared_fields')
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
            cls=MinimalPackageSerializer,
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
            cls=MinimalPackageSerializer,
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
            cls=MinimalPluginSerializer,
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
            cls=MinimalPluginSerializer,
        )
        self.assertTrue(expr=declared_fields['plugin_contributions'].child.read_only)

        self.assertIn(
            member='sub_plugins',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['sub_plugins'],
            cls=ListSerializer,
        )
        self.assertTrue(expr=declared_fields['sub_plugins'].many)
        self.assertTrue(expr=declared_fields['sub_plugins'].read_only)
        self.assertIsInstance(
            obj=declared_fields['sub_plugins'].child,
            cls=MinimalSubPluginSerializer,
        )
        self.assertTrue(expr=declared_fields['sub_plugins'].child.read_only)

        self.assertIn(
            member='sub_plugin_contributions',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['sub_plugin_contributions'],
            cls=ListSerializer,
        )
        self.assertTrue(expr=declared_fields['sub_plugin_contributions'].many)
        self.assertTrue(expr=declared_fields['sub_plugin_contributions'].read_only)
        self.assertIsInstance(
            obj=declared_fields['sub_plugin_contributions'].child,
            cls=MinimalSubPluginSerializer,
        )
        self.assertTrue(expr=declared_fields['sub_plugin_contributions'].child.read_only)

    def test_meta_class(self):
        self.assertEqual(
            first=ForumUserRetrieveSerializer.Meta.model,
            second=ForumUser,
        )
        self.assertTupleEqual(
            tuple1=ForumUserRetrieveSerializer.Meta.fields,
            tuple2=(
                'forum_id',
                'username',
                'packages',
                'package_contributions',
                'plugins',
                'plugin_contributions',
                'sub_plugins',
                'sub_plugin_contributions',
            ),
        )


class ForumUserListSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(ForumUserListSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(ForumUserListSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=10,
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
            member='package_count',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['package_count'],
            cls=IntegerField,
        )

        self.assertIn(
            member='package_contribution_count',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['package_contribution_count'],
            cls=IntegerField,
        )

        self.assertIn(
            member='plugin_count',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['plugin_count'],
            cls=IntegerField,
        )

        self.assertIn(
            member='plugin_contribution_count',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['plugin_contribution_count'],
            cls=IntegerField,
        )

        self.assertIn(
            member='sub_plugin_count',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['sub_plugin_count'],
            cls=IntegerField,
        )

        self.assertIn(
            member='sub_plugin_contribution_count',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['sub_plugin_contribution_count'],
            cls=IntegerField,
        )

        self.assertIn(
            member='project_count',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['project_count'],
            cls=IntegerField,
        )

        self.assertIn(
            member='project_contribution_count',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['project_contribution_count'],
            cls=IntegerField,
        )

        self.assertIn(
            member='total_count',
            container=declared_fields,
        )
        self.assertIsInstance(
            obj=declared_fields['total_count'],
            cls=IntegerField,
        )

    def test_meta_class(self):
        self.assertEqual(
            first=ForumUserListSerializer.Meta.model,
            second=ForumUser,
        )
        self.assertTupleEqual(
            tuple1=ForumUserListSerializer.Meta.fields,
            tuple2=(
                'forum_id',
                'username',
                'package_count',
                'package_contribution_count',
                'plugin_count',
                'plugin_contribution_count',
                'sub_plugin_count',
                'sub_plugin_contribution_count',
                'project_count',
                'project_contribution_count',
                'total_count',
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
