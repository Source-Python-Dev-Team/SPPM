# =============================================================================
# IMPORTS
# =============================================================================
# Python
from unittest import mock

# Django
from django.test import TestCase

# Third Party Django
from rest_framework.serializers import ListSerializer

# App
from project_manager.common.api.serializers import (
    ProjectContributorSerializer,
    ProjectCreateReleaseSerializer,
    ProjectGameSerializer,
    ProjectImageSerializer,
    ProjectReleaseSerializer,
    ProjectSerializer,
    ProjectTagSerializer,
)
from project_manager.packages.api.serializers.common import (
    ReleasePackageRequirementSerializer,
)
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
)
from project_manager.plugins.api.serializers.mixins import PluginReleaseBase
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
)
from requirements.api.serializers.common import (
    ReleaseDownloadRequirementSerializer,
    ReleasePyPiRequirementSerializer,
    ReleaseVersionControlRequirementSerializer,
)


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
        target='project_manager.common.api.serializers.ProjectSerializer.get_extra_kwargs',
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
