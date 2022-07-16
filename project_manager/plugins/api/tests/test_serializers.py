# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
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
from project_manager.api.common.serializers.mixins import ProjectThroughMixin
from project_manager.packages.api.common.serializers import ReleasePackageRequirementSerializer
from project_manager.plugins.api.serializers import (
    PluginContributorSerializer,
    PluginCreateReleaseSerializer,
    PluginCreateSerializer,
    PluginGameSerializer,
    PluginImageSerializer,
    PluginReleaseDownloadRequirementSerializer,
    PluginReleasePackageRequirementSerializer,
    PluginReleasePyPiRequirementSerializer,
    PluginReleaseSerializer,
    PluginReleaseVersionControlRequirementSerializer,
    PluginSerializer,
    PluginTagSerializer,
    SubPluginPathSerializer,
)
from project_manager.plugins.api.common.serializers import MinimalPluginSerializer
from project_manager.plugins.api.serializers.mixins import PluginReleaseBase
from project_manager.plugins.helpers import PluginZipFile
from project_manager.plugins.models import (
    Plugin,
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginRelease,
    PluginReleaseDownloadRequirement,
    PluginReleasePackageRequirement,
    PluginReleasePyPiRequirement,
    PluginReleaseVersionControlRequirement,
    PluginTag,
    SubPluginPath,
)
from requirements.api.serializers.common import (
    ReleaseDownloadRequirementSerializer,
    ReleasePyPiRequirementSerializer,
    ReleaseVersionControlRequirementSerializer,
)
from test_utils.factories.plugins import PluginFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PluginContributorSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginContributorSerializer,
                ProjectContributorSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginContributorSerializer.Meta,
                ProjectContributorSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginContributorSerializer.Meta.model,
            second=PluginContributor,
        )


class PluginCreateReleaseSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginCreateReleaseSerializer,
                ProjectCreateReleaseSerializer,
            ),
        )
        self.assertTrue(
            expr=issubclass(
                PluginCreateReleaseSerializer,
                PluginReleaseBase,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginCreateReleaseSerializer.Meta,
                ProjectCreateReleaseSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginCreateReleaseSerializer.Meta.model,
            second=PluginRelease,
        )


class PluginCreateSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginCreateSerializer, PluginSerializer),
        )

    @mock.patch(
        target='project_manager.api.common.serializers.ProjectSerializer.get_extra_kwargs',
        return_value={},
    )
    def test_releases(self, _):
        obj = PluginCreateSerializer()
        self.assertIn(member='releases', container=obj.fields)
        field = obj.fields['releases']
        self.assertIsInstance(obj=field, cls=PluginCreateReleaseSerializer)
        self.assertTrue(expr=field.write_only)

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginCreateSerializer.Meta,
                PluginSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginCreateSerializer.Meta.fields,
            second=PluginSerializer.Meta.fields + ('releases',),
        )


class PluginGameSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginGameSerializer, ProjectGameSerializer),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginGameSerializer.Meta,
                ProjectGameSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginGameSerializer.Meta.model,
            second=PluginGame,
        )


class PluginImageSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginImageSerializer, ProjectImageSerializer),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginImageSerializer.Meta,
                ProjectImageSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginImageSerializer.Meta.model,
            second=PluginImage,
        )


class PluginReleaseDownloadRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleaseDownloadRequirementSerializer,
                ReleaseDownloadRequirementSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleaseDownloadRequirementSerializer.Meta,
                ReleaseDownloadRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginReleaseDownloadRequirementSerializer.Meta.model,
            second=PluginReleaseDownloadRequirement,
        )


class PluginReleasePackageRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleasePackageRequirementSerializer,
                ReleasePackageRequirementSerializer,
            ),
        )

    def test_name_field(self):
        obj = PluginReleasePackageRequirementSerializer()
        self.assertIn(member='name', container=obj.fields)
        field = obj.fields['name']
        self.assertIsInstance(obj=field, cls=ReadOnlyField)
        self.assertEqual(
            first=field.source,
            second='package_requirement.name',
        )

    def test_slug_field(self):
        obj = PluginReleasePackageRequirementSerializer()
        self.assertIn(member='slug', container=obj.fields)
        field = obj.fields['slug']
        self.assertIsInstance(obj=field, cls=ReadOnlyField)
        self.assertEqual(
            first=field.source,
            second='package_requirement.slug',
        )

    def test_version_field(self):
        obj = PluginReleasePackageRequirementSerializer()
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
                PluginReleasePackageRequirementSerializer.Meta,
                ReleasePackageRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginReleasePackageRequirementSerializer.Meta.model,
            second=PluginReleasePackageRequirement,
        )


class PluginReleasePyPiRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleasePyPiRequirementSerializer,
                ReleasePyPiRequirementSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleasePyPiRequirementSerializer.Meta,
                ReleasePyPiRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginReleasePyPiRequirementSerializer.Meta.model,
            second=PluginReleasePyPiRequirement,
        )


class PluginReleaseSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleaseSerializer,
                ProjectReleaseSerializer,
            ),
        )
        self.assertTrue(
            expr=issubclass(PluginReleaseSerializer, PluginReleaseBase),
        )

    def test_download_requirements(self):
        obj = PluginReleaseSerializer()
        self.assertIn(member='download_requirements', container=obj.fields)
        field = obj.fields['download_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=PluginReleaseDownloadRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='pluginreleasedownloadrequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_package_requirements(self):
        obj = PluginReleaseSerializer()
        self.assertIn(member='package_requirements', container=obj.fields)
        field = obj.fields['package_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=PluginReleasePackageRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='pluginreleasepackagerequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_pypi_requirements(self):
        obj = PluginReleaseSerializer()
        self.assertIn(member='pypi_requirements', container=obj.fields)
        field = obj.fields['pypi_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=PluginReleasePyPiRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='pluginreleasepypirequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_vcs_requirements(self):
        obj = PluginReleaseSerializer()
        self.assertIn(member='vcs_requirements', container=obj.fields)
        field = obj.fields['vcs_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=PluginReleaseVersionControlRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='pluginreleaseversioncontrolrequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleaseSerializer.Meta,
                ProjectReleaseSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginReleaseSerializer.Meta.model,
            second=PluginRelease,
        )


class PluginReleaseVersionControlRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleaseVersionControlRequirementSerializer,
                ReleaseVersionControlRequirementSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginReleaseVersionControlRequirementSerializer.Meta,
                ReleaseVersionControlRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginReleaseVersionControlRequirementSerializer.Meta.model,
            second=PluginReleaseVersionControlRequirement,
        )


class PluginSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(PluginSerializer, ProjectSerializer))

    def test_primary_attributes(self):
        self.assertEqual(
            first=PluginSerializer.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=PluginSerializer.release_model,
            second=PluginRelease,
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginSerializer.Meta,
                ProjectSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginSerializer.Meta.model,
            second=Plugin,
        )


class PluginTagSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginTagSerializer, ProjectTagSerializer),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PluginTagSerializer.Meta,
                ProjectTagSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PluginTagSerializer.Meta.model,
            second=PluginTag,
        )


class SubPluginPathSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginPathSerializer, ProjectThroughMixin),
        )

    def test_get_field_names(self):
        obj = SubPluginPathSerializer(
            context={
                'request': mock.Mock(
                    method='POST',
                )
            },
        )
        field_names = obj.get_field_names(
            declared_fields=[],
            info=mock.Mock(),
        )
        self.assertTupleEqual(
            tuple1=field_names,
            tuple2=(
                'allow_module',
                'allow_package_using_basename',
                'allow_package_using_init',
                'path',
            ),
        )

        obj = SubPluginPathSerializer(
            context={
                'request': mock.Mock(
                    method='PATCH',
                )
            },
        )
        field_names = obj.get_field_names(
            declared_fields=[],
            info=mock.Mock(),
        )
        self.assertTupleEqual(
            tuple1=field_names,
            tuple2=(
                'allow_module',
                'allow_package_using_basename',
                'allow_package_using_init',
            ),
        )

    def test_validate(self):
        plugin = PluginFactory()
        obj = SubPluginPathSerializer(
            context={
                'view': mock.Mock(
                    project_type='plugin',
                    project=plugin,
                )
            }
        )
        field_names = (
            'allow_module',
            'allow_package_using_basename',
            'allow_package_using_init',
        )
        attrs = {
            field_name: False for field_name in field_names
        }
        with self.assertRaises(ValidationError) as context:
            obj.validate(attrs=attrs)

        self.assertEqual(
            first=len(context.exception.detail),
            second=3,
        )
        for field_name in field_names:
            self.assertIn(
                member=field_name,
                container=context.exception.detail,
            )
            error = context.exception.detail[field_name]
            self.assertEqual(
                first=error,
                second="At least one of the 'Allow' fields must be True.",
            )
            self.assertEqual(
                first=error.code,
                second='invalid',
            )

        for field_name in field_names:
            current_attrs = dict(attrs)
            current_attrs.update({
                field_name: True,
            })
            value = obj.validate(attrs=current_attrs)
            self.assertDictEqual(
                d1=value,
                d2={**current_attrs, **{'plugin': plugin}},
            )

    def test_meta_class(self):
        self.assertEqual(
            first=SubPluginPathSerializer.Meta.model,
            second=SubPluginPath,
        )
        self.assertTupleEqual(
            tuple1=SubPluginPathSerializer.Meta.fields,
            tuple2=(
                'allow_module',
                'allow_package_using_basename',
                'allow_package_using_init',
                'path',
            )
        )


class MinimalPluginSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(MinimalPluginSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(MinimalPluginSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=0,
        )

    def test_meta_class(self):
        self.assertEqual(
            first=MinimalPluginSerializer.Meta.model,
            second=Plugin,
        )
        self.assertTupleEqual(
            tuple1=MinimalPluginSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
            ),
        )


class PluginReleaseBaseTestCase(TestCase):
    def test_base_attributes(self):
        self.assertEqual(
            first=PluginReleaseBase.project_class,
            second=Plugin,
        )
        self.assertEqual(
            first=PluginReleaseBase.project_type,
            second='plugin',
        )

    def test_zip_parser(self):
        self.assertEqual(
            first=PluginReleaseBase().zip_parser,
            second=PluginZipFile,
        )

    def test_get_project_kwargs(self):
        obj = PluginReleaseBase()
        slug = 'test-plugin'
        obj.context = {
            'view': mock.Mock(
                kwargs={'plugin_slug': slug},
            ),
        }
        self.assertDictEqual(
            d1=obj.get_project_kwargs(),
            d2={'pk': slug},
        )
