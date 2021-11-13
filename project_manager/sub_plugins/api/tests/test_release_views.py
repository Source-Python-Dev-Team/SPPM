# =============================================================================
# IMPORTS
# =============================================================================
# Python
import shutil
import tempfile

# Django
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.test import override_settings
from django.utils import formats

# Third Party Python
from path import Path

# Third Party Django
from rest_framework import status
from rest_framework.parsers import ParseError
from rest_framework.test import APITestCase

# App
from project_manager.common.api.views import ProjectReleaseViewSet
from project_manager.sub_plugins.api.serializers import SubPluginReleaseSerializer
from project_manager.sub_plugins.api.views import SubPluginReleaseViewSet
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginRelease,
    SubPluginReleaseDownloadRequirement,
    SubPluginReleasePackageRequirement,
    SubPluginReleasePyPiRequirement,
    SubPluginReleaseVersionControlRequirement,
)
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from test_utils.factories.packages import PackageFactory, PackageReleaseFactory
from test_utils.factories.plugins import PluginFactory, SubPluginPathFactory
from test_utils.factories.sub_plugins import (
    SubPluginContributorFactory,
    SubPluginFactory,
    SubPluginReleaseFactory,
)
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginReleaseViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = plugin = sub_plugin = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory()
        cls.sub_plugin = SubPluginFactory(
            owner=cls.owner,
            plugin=cls.plugin,
        )
        cls.base_api_path = f'/api/sub-plugins/releases/'
        cls.api_path = f'{cls.base_api_path}{cls.plugin.slug}/{cls.sub_plugin.slug}/'
        cls.contributor = ForumUserFactory()
        SubPluginContributorFactory(
            sub_plugin=cls.sub_plugin,
            user=cls.contributor,
        )
        cls.sub_plugin_release = SubPluginReleaseFactory(
            sub_plugin=cls.sub_plugin,
            zip_file='release_v1.0.0.zip',
        )
        cls.regular_user = ForumUserFactory()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginReleaseViewSet, ProjectReleaseViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginReleaseViewSet.serializer_class,
            second=SubPluginReleaseSerializer,
        )
        self.assertEqual(
            first=SubPluginReleaseViewSet.project_type,
            second='sub-plugin',
        )
        self.assertEqual(
            first=SubPluginReleaseViewSet.project_model,
            second=SubPlugin,
        )
        self.assertIs(
            expr1=SubPluginReleaseViewSet.queryset.model,
            expr2=SubPluginRelease,
        )
        self.assertDictEqual(
            d1=SubPluginReleaseViewSet.queryset.query.select_related,
            d2={'sub_plugin': {}},
        )
        prefetch_lookups = SubPluginReleaseViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=4)

        lookup = prefetch_lookups[0]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='subpluginreleasepackagerequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=SubPluginReleasePackageRequirement,
        )
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('package_requirement__name',),
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'package_requirement': {}},
        )

        lookup = prefetch_lookups[1]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='subpluginreleasedownloadrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=SubPluginReleaseDownloadRequirement,
        )
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('download_requirement__url',),
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'download_requirement': {}},
        )

        lookup = prefetch_lookups[2]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='subpluginreleasepypirequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=SubPluginReleasePyPiRequirement,
        )
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('pypi_requirement__name',),
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'pypi_requirement': {}},
        )

        lookup = prefetch_lookups[3]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='subpluginreleaseversioncontrolrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=SubPluginReleaseVersionControlRequirement,
        )
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('vcs_requirement__url',),
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'vcs_requirement': {}},
        )

    def test_parent_project(self):
        obj = SubPluginReleaseViewSet()
        invalid_slug = 'invalid'
        obj.kwargs = {'plugin_slug': invalid_slug}
        with self.assertRaises(ParseError) as context:
            _ = obj.parent_project

        self.assertEqual(
            first=context.exception.detail,
            second=f"Plugin '{invalid_slug}' not found.",
        )

        plugin = PluginFactory()
        obj.kwargs = {'plugin_slug': plugin.slug}
        self.assertEqual(
            first=obj.parent_project,
            second=plugin,
        )

    def test_get_project_kwargs(self):
        obj = SubPluginReleaseViewSet()
        plugin = PluginFactory()
        sub_plugin_slug = 'test-sub-plugin'
        obj.kwargs = {
            'sub_plugin_slug': sub_plugin_slug,
            'plugin_slug': plugin.slug,
        }
        self.assertDictEqual(
            d1=obj.get_project_kwargs(),
            d2={
                'slug': sub_plugin_slug,
                'plugin': plugin,
            }
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=SubPluginReleaseViewSet.http_method_names,
            tuple2=('get', 'post', 'options'),
        )

    def test_get_list(self):
        # Verify that a non logged in user can see results
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=1)
        timestamp = self.sub_plugin_release.created
        request = response.wsgi_request
        zip_file = f'{request.scheme}://{request.get_host()}{self.sub_plugin_release.zip_file.url}'
        payload = {
            'notes': self.sub_plugin_release.notes,
            'zip_file': zip_file,
            'version': self.sub_plugin_release.version,
            'created': {
                'actual': timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'locale': formats.date_format(timestamp, 'DATETIME_FORMAT'),
                'locale_short': formats.date_format(timestamp, 'SHORT_DATETIME_FORMAT'),
            },
            'download_count': self.sub_plugin_release.download_count,
            'download_requirements': [],
            'package_requirements': [],
            'pypi_requirements': [],
            'vcs_requirements': [],
            'id': str(self.sub_plugin_release.id),
        }
        self.assertDictEqual(
            d1=content['results'][0],
            d2=payload,
        )

        # Verify that regular user can see results
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=1)
        self.assertDictEqual(
            d1=content['results'][0],
            d2=payload,
        )

        # Verify that contributors can see results
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=1)
        self.assertDictEqual(
            d1=content['results'][0],
            d2=payload,
        )

        # Verify that the owner can see results
        self.client.force_login(self.owner.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=1)
        self.assertDictEqual(
            d1=content['results'][0],
            d2=payload,
        )

    def test_get_details(self):
        # Verify that non logged in user can see details
        api_path = f'{self.api_path}{self.sub_plugin_release.version}/'
        response = self.client.get(path=api_path)
        timestamp = self.sub_plugin_release.created
        request = response.wsgi_request
        zip_file = f'{request.scheme}://{request.get_host()}{self.sub_plugin_release.zip_file.url}'
        payload = {
            'notes': self.sub_plugin_release.notes,
            'zip_file': zip_file,
            'version': self.sub_plugin_release.version,
            'created': {
                'actual': timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'locale': formats.date_format(timestamp, 'DATETIME_FORMAT'),
                'locale_short': formats.date_format(timestamp, 'SHORT_DATETIME_FORMAT'),
            },
            'download_count': self.sub_plugin_release.download_count,
            'download_requirements': [],
            'package_requirements': [],
            'pypi_requirements': [],
            'vcs_requirements': [],
            'id': str(self.sub_plugin_release.id),
        }
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2=payload,
        )

        # Verify that regular user can see details
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2=payload,
        )

        # Verify that contributors can see details
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2=payload,
        )

        # Verify that the owner can see details
        self.client.force_login(self.owner.user)
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2=payload,
        )

    def test_get_details_failure(self):
        api_path = f'{self.base_api_path}{self.plugin.slug}/invalid/'
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid sub_plugin_slug.'},
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post(self):
        plugin = PluginFactory(
            basename='test_plugin',
        )
        SubPluginPathFactory(
            plugin=plugin,
            path='sub_plugins',
            allow_package_using_basename=True,
        )
        sub_plugin = SubPluginFactory(
            plugin=plugin,
            basename='test_sub_plugin',
            owner=self.owner,
        )
        SubPluginReleaseFactory(
            sub_plugin=sub_plugin,
            version='1.0.0',
        )
        SubPluginContributorFactory(
            sub_plugin=sub_plugin,
            user=self.contributor,
        )
        api_path = f'{self.base_api_path}{plugin.slug}/{sub_plugin.slug}/'
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'sub-plugins'
        file_path = base_path / 'test-plugin' / 'test-sub-plugin' / 'test-sub-plugin-v1.0.0.zip'

        # Verify that non logged in user cannot create a release
        version = '1.0.1'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=api_path,
                data={
                    'version': version,
                    'zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot create a release
        version = '1.0.1'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            self.client.force_login(self.regular_user.user)
            response = self.client.post(
                path=api_path,
                data={
                    'version': version,
                    'zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify contributor can create a release
        version = '1.0.1'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            self.client.force_login(self.contributor.user)
            response = self.client.post(
                path=api_path,
                data={
                    'version': version,
                    'zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )
        self.assertEqual(
            first=sub_plugin.releases.count(),
            second=2,
        )
        content = response.json()
        release = sub_plugin.releases.get(pk=content['id'])
        self.assertEqual(
            first=release.version,
            second=version,
        )

        # Verify owner can create a release
        version = '1.0.2'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            self.client.force_login(self.owner.user)
            response = self.client.post(
                path=api_path,
                data={
                    'version': version,
                    'zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )
        self.assertEqual(
            first=sub_plugin.releases.count(),
            second=3,
        )
        content = response.json()
        release = sub_plugin.releases.get(pk=content['id'])
        self.assertEqual(
            first=release.version,
            second=version,
        )

        # Verify that the same version cannot be created twice
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=api_path,
                data={
                    'version': version,
                    'zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'version': ['Given version matches existing version.']},
        )

        # Verify that the basename in the zip file is being verified against
        #   the basename from the url path
        zip_basename = sub_plugin.basename
        sub_plugin = SubPluginFactory(
            plugin=plugin,
            owner=self.owner,
        )
        SubPluginReleaseFactory(
            sub_plugin=sub_plugin,
            version='1.0.0',
        )
        api_path = f'{self.base_api_path}{plugin.slug}/{sub_plugin.slug}/'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=api_path,
                data={
                    'version': version,
                    'zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'zip_file': [
                    f"Basename in zip '{zip_basename}' does not match basename"
                    f" for sub-plugin '{sub_plugin.basename}'.",
                ],
            }
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post_with_requirements(self):
        plugin = PluginFactory(
            basename='test_plugin',
        )
        SubPluginPathFactory(
            plugin=plugin,
            path='sub_plugins',
            allow_package_using_basename=True,
        )
        sub_plugin = SubPluginFactory(
            plugin=plugin,
            basename='test_sub_plugin',
            owner=self.owner,
        )
        SubPluginReleaseFactory(
            sub_plugin=sub_plugin,
            version='1.0.0',
        )
        api_path = f'{self.base_api_path}{plugin.slug}/{sub_plugin.slug}/'
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'sub-plugins'
        file_path = base_path / 'test-plugin' / 'test-sub-plugin' / 'test-sub-plugin-requirements-v1.0.0.zip'
        version = '1.0.1'
        custom_package_1 = PackageFactory(
            basename='custom_package_1',
        )
        PackageReleaseFactory(
            package=custom_package_1,
            version='1.0.0',
        )
        custom_package_2 = PackageFactory(
            basename='custom_package_2',
        )
        PackageReleaseFactory(
            package=custom_package_2,
            version='1.0.0',
        )
        self.assertEqual(
            first=DownloadRequirement.objects.count(),
            second=0,
        )
        self.assertEqual(
            first=PyPiRequirement.objects.count(),
            second=0,
        )
        self.assertEqual(
            first=VersionControlRequirement.objects.count(),
            second=0,
        )
        self.client.force_login(self.owner.user)
        package = PackageFactory(
            basename='test_package',
            owner=self.owner,
        )
        PackageReleaseFactory(
            package=package,
            version='1.0.0',
        )
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=api_path,
                data={
                    'version': version,
                    'zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )
        release = SubPluginRelease.objects.get(pk=response.json()['id'])
        self.assertEqual(
            first=DownloadRequirement.objects.count(),
            second=2,
        )
        self.assertEqual(
            first=release.download_requirements.count(),
            second=2,
        )
        self.assertEqual(
            first=PyPiRequirement.objects.count(),
            second=2,
        )
        self.assertEqual(
            first=release.pypi_requirements.count(),
            second=2,
        )
        self.assertEqual(
            first=VersionControlRequirement.objects.count(),
            second=2,
        )
        self.assertEqual(
            first=release.vcs_requirements.count(),
            second=2,
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second=f'{self.sub_plugin} - Release',
        )
