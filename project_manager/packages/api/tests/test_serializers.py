# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
from django.test import TestCase

# Third Party Django
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
from project_manager.packages.api.serializers import (
    PackageContributorSerializer,
    PackageCreateReleaseSerializer,
    PackageCreateSerializer,
    PackageGameSerializer,
    PackageImageSerializer,
    PackageReleaseDownloadRequirementSerializer,
    PackageReleasePackageRequirementSerializer,
    PackageReleasePyPiRequirementSerializer,
    PackageReleaseSerializer,
    PackageReleaseVersionControlRequirementSerializer,
    PackageSerializer,
    PackageTagSerializer,
)
from project_manager.packages.api.common.serializers import (
    MinimalPackageSerializer,
    ReleasePackageRequirementSerializer,
)
from project_manager.packages.api.serializers.mixins import PackageReleaseBase
from project_manager.packages.helpers import PackageZipFile
from project_manager.packages.models import (
    Package,
    PackageContributor,
    PackageGame,
    PackageImage,
    PackageRelease,
    PackageReleaseDownloadRequirement,
    PackageReleasePackageRequirement,
    PackageReleasePyPiRequirement,
    PackageReleaseVersionControlRequirement,
    PackageTag,
)
from requirements.api.serializers.common import (
    ReleaseDownloadRequirementSerializer,
    ReleasePyPiRequirementSerializer,
    ReleaseVersionControlRequirementSerializer,
)


# =============================================================================
# TEST CASES
# =============================================================================
class PackageContributorSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageContributorSerializer,
                ProjectContributorSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageContributorSerializer.Meta,
                ProjectContributorSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageContributorSerializer.Meta.model,
            second=PackageContributor,
        )


class PackageCreateReleaseSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageCreateReleaseSerializer,
                ProjectCreateReleaseSerializer,
            ),
        )
        self.assertTrue(
            expr=issubclass(
                PackageCreateReleaseSerializer,
                PackageReleaseBase,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageCreateReleaseSerializer.Meta,
                ProjectCreateReleaseSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageCreateReleaseSerializer.Meta.model,
            second=PackageRelease,
        )


class PackageCreateSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageCreateSerializer, PackageSerializer),
        )

    @mock.patch(
        target='project_manager.api.common.serializers.ProjectSerializer.get_extra_kwargs',
        return_value={},
    )
    def test_releases(self, _):
        obj = PackageCreateSerializer()
        self.assertIn(member='releases', container=obj.fields)
        field = obj.fields['releases']
        self.assertIsInstance(obj=field, cls=PackageCreateReleaseSerializer)
        self.assertTrue(expr=field.write_only)

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageCreateSerializer.Meta,
                PackageSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageCreateSerializer.Meta.fields,
            second=PackageSerializer.Meta.fields + ('releases',),
        )


class PackageGameSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageGameSerializer, ProjectGameSerializer),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageGameSerializer.Meta,
                ProjectGameSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageGameSerializer.Meta.model,
            second=PackageGame,
        )


class PackageImageSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageImageSerializer, ProjectImageSerializer),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageImageSerializer.Meta,
                ProjectImageSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageImageSerializer.Meta.model,
            second=PackageImage,
        )


class PackageReleaseDownloadRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleaseDownloadRequirementSerializer,
                ReleaseDownloadRequirementSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleaseDownloadRequirementSerializer.Meta,
                ReleaseDownloadRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageReleaseDownloadRequirementSerializer.Meta.model,
            second=PackageReleaseDownloadRequirement,
        )


class PackageReleasePackageRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleasePackageRequirementSerializer,
                ReleasePackageRequirementSerializer,
            ),
        )

    def test_name_field(self):
        obj = PackageReleasePackageRequirementSerializer()
        self.assertIn(member='name', container=obj.fields)
        field = obj.fields['name']
        self.assertIsInstance(obj=field, cls=ReadOnlyField)
        self.assertEqual(
            first=field.source,
            second='package_requirement.name',
        )

    def test_slug_field(self):
        obj = PackageReleasePackageRequirementSerializer()
        self.assertIn(member='slug', container=obj.fields)
        field = obj.fields['slug']
        self.assertIsInstance(obj=field, cls=ReadOnlyField)
        self.assertEqual(
            first=field.source,
            second='package_requirement.slug',
        )

    def test_version_field(self):
        obj = PackageReleasePackageRequirementSerializer()
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
                PackageReleasePackageRequirementSerializer.Meta,
                ReleasePackageRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageReleasePackageRequirementSerializer.Meta.model,
            second=PackageReleasePackageRequirement,
        )


class PackageReleasePyPiRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleasePyPiRequirementSerializer,
                ReleasePyPiRequirementSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleasePyPiRequirementSerializer.Meta,
                ReleasePyPiRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageReleasePyPiRequirementSerializer.Meta.model,
            second=PackageReleasePyPiRequirement,
        )


class PackageReleaseSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleaseSerializer,
                ProjectReleaseSerializer,
            ),
        )
        self.assertTrue(
            expr=issubclass(PackageReleaseSerializer, PackageReleaseBase),
        )

    def test_download_requirements(self):
        obj = PackageReleaseSerializer()
        self.assertIn(member='download_requirements', container=obj.fields)
        field = obj.fields['download_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=PackageReleaseDownloadRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='packagereleasedownloadrequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_package_requirements(self):
        obj = PackageReleaseSerializer()
        self.assertIn(member='package_requirements', container=obj.fields)
        field = obj.fields['package_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=PackageReleasePackageRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='packagereleasepackagerequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_pypi_requirements(self):
        obj = PackageReleaseSerializer()
        self.assertIn(member='pypi_requirements', container=obj.fields)
        field = obj.fields['pypi_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=PackageReleasePyPiRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='packagereleasepypirequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_vcs_requirements(self):
        obj = PackageReleaseSerializer()
        self.assertIn(member='vcs_requirements', container=obj.fields)
        field = obj.fields['vcs_requirements']
        self.assertIsInstance(obj=field, cls=ListSerializer)
        self.assertTrue(expr=field.many)
        self.assertTrue(expr=field.read_only)
        self.assertIsInstance(
            obj=field.child,
            cls=PackageReleaseVersionControlRequirementSerializer,
        )
        self.assertEqual(
            first=field.source,
            second='packagereleaseversioncontrolrequirement_set',
        )
        self.assertTrue(expr=field.child.read_only)

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleaseSerializer.Meta,
                ProjectReleaseSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageReleaseSerializer.Meta.model,
            second=PackageRelease,
        )


class PackageReleaseVersionControlRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleaseVersionControlRequirementSerializer,
                ReleaseVersionControlRequirementSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageReleaseVersionControlRequirementSerializer.Meta,
                ReleaseVersionControlRequirementSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageReleaseVersionControlRequirementSerializer.Meta.model,
            second=PackageReleaseVersionControlRequirement,
        )


class PackageSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(PackageSerializer, ProjectSerializer))

    def test_primary_attributes(self):
        self.assertEqual(
            first=PackageSerializer.project_type,
            second='package',
        )
        self.assertEqual(
            first=PackageSerializer.release_model,
            second=PackageRelease,
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageSerializer.Meta,
                ProjectSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageSerializer.Meta.model,
            second=Package,
        )


class PackageTagSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageTagSerializer, ProjectTagSerializer),
        )

    def test_meta_class(self):
        self.assertTrue(
            expr=issubclass(
                PackageTagSerializer.Meta,
                ProjectTagSerializer.Meta,
            ),
        )
        self.assertEqual(
            first=PackageTagSerializer.Meta.model,
            second=PackageTag,
        )


class ReleasePackageRequirementSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                ReleasePackageRequirementSerializer,
                ModelSerializer,
            ),
        )

    def test_meta_class(self):
        self.assertTupleEqual(
            tuple1=ReleasePackageRequirementSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
                'version',
                'optional',
            ),
        )


class MinimalPackageSerializerTestCase(TestCase):
    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(MinimalPackageSerializer, ModelSerializer),
        )

    def test_declared_fields(self):
        declared_fields = getattr(MinimalPackageSerializer, '_declared_fields')
        self.assertEqual(
            first=len(declared_fields),
            second=0,
        )

    def test_meta_class(self):
        self.assertEqual(
            first=MinimalPackageSerializer.Meta.model,
            second=Package,
        )
        self.assertTupleEqual(
            tuple1=MinimalPackageSerializer.Meta.fields,
            tuple2=(
                'name',
                'slug',
            ),
        )


class PackageReleaseBaseTestCase(TestCase):
    def test_base_attributes(self):
        self.assertEqual(
            first=PackageReleaseBase.project_class,
            second=Package,
        )
        self.assertEqual(
            first=PackageReleaseBase.project_type,
            second='package',
        )

    def test_zip_parser(self):
        self.assertEqual(
            first=PackageReleaseBase().zip_parser,
            second=PackageZipFile,
        )

    def test_get_project_kwargs(self):
        obj = PackageReleaseBase()
        slug = 'test-package'
        obj.context = {
            'view': mock.Mock(
                kwargs={'package_slug': slug},
            ),
        }
        self.assertDictEqual(
            d1=obj.get_project_kwargs(),
            d2={'pk': slug},
        )
