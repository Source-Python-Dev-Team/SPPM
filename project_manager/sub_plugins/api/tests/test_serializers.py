# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
from django.conf import settings
from django.test import TestCase

# Third Party Django
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ListSerializer, ModelSerializer

# App
from project_manager.api.common.serializers import (
    ProjectContributorSerializer,
    ProjectCreateReleaseSerializer,
    ProjectGameSerializer,
    ProjectImageSerializer,
    ProjectReleaseSerializer,
    ProjectSerializer,
    ProjectTagSerializer,
)
from project_manager.packages.api.common.serializers import ReleasePackageRequirementSerializer
from project_manager.plugins.api.common.serializers import MinimalPluginSerializer
from project_manager.sub_plugins.api.serializers import (
    SubPluginContributorSerializer,
    SubPluginCreateReleaseSerializer,
    SubPluginCreateSerializer,
    SubPluginGameSerializer,
    SubPluginImageSerializer,
    SubPluginReleaseDownloadRequirementSerializer,
    SubPluginReleasePackageRequirementSerializer,
    SubPluginReleasePyPiRequirementSerializer,
    SubPluginReleaseSerializer,
    SubPluginReleaseVersionControlRequirementSerializer,
    SubPluginSerializer,
    SubPluginTagSerializer,
)
from project_manager.sub_plugins.api.common.serializers import MinimalSubPluginSerializer
from project_manager.sub_plugins.api.serializers.mixins import SubPluginReleaseBase
from project_manager.sub_plugins.helpers import SubPluginZipFile
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginContributor,
    SubPluginGame,
    SubPluginImage,
    SubPluginRelease,
    SubPluginReleaseDownloadRequirement,
    SubPluginReleasePackageRequirement,
    SubPluginReleasePyPiRequirement,
    SubPluginReleaseVersionControlRequirement,
    SubPluginTag,
)
from requirements.api.serializers.common import (
    ReleaseDownloadRequirementSerializer,
    ReleasePyPiRequirementSerializer,
    ReleaseVersionControlRequirementSerializer,
)
from test_utils.factories.plugins import PluginFactory
from test_utils.factories.sub_plugins import SubPluginReleaseFactory
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginContributorSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginContributorSerializer,
                ProjectContributorSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginContributorSerializer.Meta,
                ProjectContributorSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginContributorSerializer.Meta.model,
            second=SubPluginContributor,
        )


class SubPluginCreateReleaseSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginCreateReleaseSerializer,
                ProjectCreateReleaseSerializer,
            ),
        )
        self.assertTrue(
            expr=issubclass(
                SubPluginCreateReleaseSerializer,
                SubPluginReleaseBase,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginCreateReleaseSerializer.Meta,
                ProjectCreateReleaseSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginCreateReleaseSerializer.Meta.model,
            second=SubPluginRelease,
        )


class SubPluginCreateSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginCreateSerializer, SubPluginSerializer),
        )

    def test_releases(self):
        mock.patch(
            target=(
                'project_manager.api.common.serializers.ProjectSerializer.'
                'get_extra_kwargs'
            ),
            return_value={},
        ).start()
        obj = SubPluginCreateSerializer()
        obj.context['view'] = mock.Mock(
            action='list',
        )
        self.assertIn(member='releases', container=obj.fields)
        field = obj.fields['releases']
        self.assertIsInstance(obj=field, cls=SubPluginCreateReleaseSerializer)
        self.assertTrue(expr=field.write_only)

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginCreateSerializer.Meta,
                SubPluginSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginCreateSerializer.Meta.fields,
            second=SubPluginSerializer.Meta.fields + ('releases',),
        )


class SubPluginGameSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginGameSerializer, ProjectGameSerializer),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginGameSerializer.Meta,
                ProjectGameSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginGameSerializer.Meta.model,
            second=SubPluginGame,
        )


class SubPluginImageSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginImageSerializer, ProjectImageSerializer),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginImageSerializer.Meta,
                ProjectImageSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginImageSerializer.Meta.model,
            second=SubPluginImage,
        )


class SubPluginReleaseDownloadRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleaseDownloadRequirementSerializer,
                ReleaseDownloadRequirementSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleaseDownloadRequirementSerializer.Meta,
                ReleaseDownloadRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginReleaseDownloadRequirementSerializer.Meta.model,
            second=SubPluginReleaseDownloadRequirement,
        )


class SubPluginReleasePackageRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleasePackageRequirementSerializer,
                ReleasePackageRequirementSerializer,
            ),
        )

    def test_name_field(self):
        obj = SubPluginReleasePackageRequirementSerializer()
        self.assertIn(member='name', container=obj.fields)
        field = obj.fields['name']
        self.assertIsInstance(obj=field, cls=ReadOnlyField)
        self.assertEqual(
            first=field.source,
            second='package_requirement.name',
        )

    def test_slug_field(self):
        obj = SubPluginReleasePackageRequirementSerializer()
        self.assertIn(member='slug', container=obj.fields)
        field = obj.fields['slug']
        self.assertIsInstance(obj=field, cls=ReadOnlyField)
        self.assertEqual(
            first=field.source,
            second='package_requirement.slug',
        )

    def test_version_field(self):
        obj = SubPluginReleasePackageRequirementSerializer()
        self.assertIn(member='version', container=obj.fields)
        field = obj.fields['version']
        self.assertIsInstance(obj=field, cls=ReadOnlyField)
        self.assertEqual(
            first=field.source,
            second='version',
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleasePackageRequirementSerializer.Meta,
                ReleasePackageRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginReleasePackageRequirementSerializer.Meta.model,
            second=SubPluginReleasePackageRequirement,
        )


class SubPluginReleasePyPiRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleasePyPiRequirementSerializer,
                ReleasePyPiRequirementSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleasePyPiRequirementSerializer.Meta,
                ReleasePyPiRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginReleasePyPiRequirementSerializer.Meta.model,
            second=SubPluginReleasePyPiRequirement,
        )


class SubPluginReleaseSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleaseSerializer,
                ProjectReleaseSerializer,
            ),
        )
        self.assertTrue(
            expr=issubclass(SubPluginReleaseSerializer, SubPluginReleaseBase),
        )

    def test_download_requirements(self):
        obj = SubPluginReleaseSerializer()
        self.assertIn(member='download_requirements', container=obj.fields)
        field = obj.fields['download_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=SubPluginReleaseDownloadRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='subpluginreleasedownloadrequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_package_requirements(self):
        obj = SubPluginReleaseSerializer()
        self.assertIn(member='package_requirements', container=obj.fields)
        field = obj.fields['package_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=SubPluginReleasePackageRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='subpluginreleasepackagerequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_pypi_requirements(self):
        obj = SubPluginReleaseSerializer()
        self.assertIn(member='pypi_requirements', container=obj.fields)
        field = obj.fields['pypi_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=SubPluginReleasePyPiRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='subpluginreleasepypirequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_vcs_requirements(self):
        obj = SubPluginReleaseSerializer()
        self.assertIn(member='vcs_requirements', container=obj.fields)
        field = obj.fields['vcs_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=SubPluginReleaseVersionControlRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='subpluginreleaseversioncontrolrequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleaseSerializer.Meta,
                ProjectReleaseSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginReleaseSerializer.Meta.model,
            second=SubPluginRelease,
        )


class SubPluginReleaseVersionControlRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleaseVersionControlRequirementSerializer,
                ReleaseVersionControlRequirementSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginReleaseVersionControlRequirementSerializer.Meta,
                ReleaseVersionControlRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginReleaseVersionControlRequirementSerializer.Meta.model,
            second=SubPluginReleaseVersionControlRequirement,
        )


class SubPluginSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginSerializer, ProjectSerializer))

    def test_primary_attributes(self):
        self.assertEqual(
            first=SubPluginSerializer.project_type,
            second='sub-plugin',
        )
        self.assertEqual(
            first=SubPluginSerializer.release_model,
            second=SubPluginRelease,
        )

    def test_get_fields(self):
        obj = SubPluginSerializer()
        obj.context['view'] = mock.Mock(
            action='list',
        )
        fields = obj.get_fields()
        self.assertSetEqual(
            set1=set(fields.keys()),
            set2={
                'name',
                'slug',
                'total_downloads',
                'current_release',
                'created',
                'updated',
                'synopsis',
                'description',
                'configuration',
                'logo',
                'video',
                'owner',
                'contributors',
            },
        )

        obj = SubPluginSerializer()
        obj.context['view'] = mock.Mock(
            action='retrieve',
        )
        fields = obj.get_fields()
        self.assertSetEqual(
            set1=set(fields.keys()),
            set2={
                'name',
                'slug',
                'total_downloads',
                'current_release',
                'created',
                'updated',
                'synopsis',
                'description',
                'configuration',
                'logo',
                'video',
                'owner',
            },
        )

    def test_parent_project(self):
        obj = SubPluginSerializer()
        invalid_plugin_slug = 'invalid'
        obj.context['view'] = mock.Mock(
            kwargs={'plugin_slug': invalid_plugin_slug},
        )
        with self.assertRaises(ValidationError) as context:
            _ = obj.parent_project

        self.assertEqual(
            first=len(context.exception.detail),
            second=1,
        )
        self.assertIn(
            member='plugin',
            container=context.exception.detail,
        )
        error = context.exception.detail['plugin']
        self.assertEqual(
            first=error,
            second=f"Plugin '{invalid_plugin_slug}' not found.",
        )
        self.assertEqual(
            first=error.code,
            second='invalid',
        )

        plugin_basename = 'test_plugin'
        plugin_slug = plugin_basename.replace('_', '-')
        plugin = PluginFactory(
            basename=plugin_basename,
        )
        obj.context['view'] = mock.Mock(
            kwargs={'plugin_slug': plugin_slug},
        )
        parent_obj = obj.parent_project
        self.assertEqual(
            first=parent_obj.basename,
            second=plugin.basename,
        )

    def test_get_download_kwargs(self):
        zip_file = settings.MEDIA_ROOT / 'releases' / 'file_name_v1.0.0.zip'
        zip_file = zip_file.replace('\\', '/')
        release = SubPluginReleaseFactory(
            zip_file=zip_file,
        )
        obj = release.sub_plugin
        instance = SubPluginSerializer()
        kwargs = instance.get_download_kwargs(obj=obj, release=release)
        self.assertDictEqual(
            d1=kwargs,
            d2={
                'slug': obj.plugin.slug,
                'sub_plugin_slug': obj.slug,
                'zip_file': release.file_name,
            },
        )

    def test_get_extra_validated_data(self):
        forum_user = ForumUserFactory()
        obj = SubPluginSerializer()
        obj.context['request'] = mock.Mock(
            user=forum_user.user,
        )
        plugin_basename = 'test_plugin'
        plugin_slug = plugin_basename.replace('_', '-')
        plugin = PluginFactory(
            basename=plugin_basename,
        )
        obj.context['view'] = mock.Mock(
            kwargs={'plugin_slug': plugin_slug},
        )
        obj_basename = 'test_sub_plugin'
        obj.release_dict = {
            'basename': obj_basename,
        }
        original_validated_data = {}
        validated_data = obj.get_extra_validated_data(
            validated_data=original_validated_data,
        )
        self.assertDictEqual(
            d1=validated_data,
            d2={
                'owner': forum_user,
                'basename': obj_basename,
                'plugin': plugin,
            }
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginSerializer.Meta,
                ProjectSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginSerializer.Meta.model,
            second=SubPlugin,
        )


class SubPluginTagSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginTagSerializer, ProjectTagSerializer),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginTagSerializer.Meta,
                ProjectTagSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=SubPluginTagSerializer.Meta.model,
            second=SubPluginTag,
        )


class MinimalSubPluginSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(MinimalSubPluginSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(MinimalSubPluginSerializer, '_declared_fields')
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
            cls=MinimalPluginSerializer,
        )

    def test_meta_class(self):
        self.assertEqual(
            first=MinimalSubPluginSerializer.Meta.model,
            second=SubPlugin,
        )
        self.assertTupleEqual(
            tuple1=MinimalSubPluginSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
                'plugin',
            ),
        )


class SubPluginReleaseBaseTestCase(TestCase):
    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginReleaseBase.project_class,
            second=SubPlugin,
        )
        self.assertEqual(
            first=SubPluginReleaseBase.project_type,
            second='sub-plugin',
        )

    def test_parent_project(self):
        obj = SubPluginReleaseBase()
        invalid_slug = 'invalid'
        obj.context = {
            'view': mock.Mock(
                kwargs={'plugin_slug': invalid_slug},
            ),
        }
        with self.assertRaises(ValidationError) as context:
            _ = obj.parent_project

        self.assertEqual(
            first=len(context.exception.detail),
            second=1,
        )
        self.assertEqual(
            first=context.exception.detail[0],
            second=f"Plugin '{invalid_slug}' not found.",
        )

        plugin = PluginFactory()
        obj.context = {
            'view': mock.Mock(
                kwargs={'plugin_slug': plugin.slug},
            ),
        }
        self.assertEqual(
            first=obj.parent_project,
            second=plugin,
        )

    def test_zip_parser(self):
        self.assertEqual(
            first=SubPluginReleaseBase().zip_parser,
            second=SubPluginZipFile,
        )

    def test_get_project_kwargs(self):
        obj = SubPluginReleaseBase()
        plugin = PluginFactory()
        slug = 'test-sub-plugin'
        obj.context = {
            'view': mock.Mock(
                kwargs={
                    'sub_plugin_slug': slug,
                    'plugin_slug': plugin.slug,
                },
            ),
        }
        self.assertDictEqual(
            d1=obj.get_project_kwargs(),
            d2={
                'slug': slug,
                'plugin': plugin,
            },
        )
