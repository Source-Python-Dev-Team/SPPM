# =============================================================================
# IMPORTS
# =============================================================================
# Python
import shutil
import tempfile
from copy import deepcopy

# Django
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import connection
from django.test import override_settings
from django.utils import formats

# Third Party Python
from path import Path

# Third Party Django
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.api.common.views import ProjectReleaseViewSet
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
    SubPluginReleaseDownloadRequirementFactory,
    SubPluginReleaseFactory,
    SubPluginReleasePackageRequirementFactory,
    SubPluginReleasePyPiRequirementFactory,
    SubPluginReleaseVersionControlRequirementFactory,
)
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginReleaseViewSetTestCase(APITestCase):

    contributor = detail_api = list_api = owner = plugin = sub_plugin_1 = None
    sub_plugin_2 = sub_plugin_release_1 = sub_plugin_release_2 = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            basename='test_plugin',
        )
        SubPluginPathFactory(
            plugin=cls.plugin,
            path='sub_plugins',
            allow_package_using_basename=True,
        )
        cls.sub_plugin_1 = SubPluginFactory(
            basename='test_sub_plugin',
            owner=cls.owner,
            plugin=cls.plugin,
        )
        cls.sub_plugin_2 = SubPluginFactory(
            basename='test_sub_plugin_2',
            owner=cls.owner,
            plugin=cls.plugin,
        )
        cls.contributor = ForumUserFactory()
        SubPluginContributorFactory(
            sub_plugin=cls.sub_plugin_1,
            user=cls.contributor,
        )
        SubPluginContributorFactory(
            sub_plugin=cls.sub_plugin_2,
            user=cls.contributor,
        )
        cls.sub_plugin_release_1 = SubPluginReleaseFactory(
            sub_plugin=cls.sub_plugin_1,
            version='1.0.0',
            zip_file='release_v1.0.0.zip',
        )
        cls.sub_plugin_release_2 = SubPluginReleaseFactory(
            sub_plugin=cls.sub_plugin_1,
            version='1.0.1',
            zip_file='release_v1.0.1.zip',
        )
        download_requirement_1 = SubPluginReleaseDownloadRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_1,
        )
        download_requirement_2 = SubPluginReleaseDownloadRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_1,
        )
        download_requirement_3 = SubPluginReleaseDownloadRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_2,
        )
        package_requirement_1 = SubPluginReleasePackageRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_1,
        )
        package_requirement_2 = SubPluginReleasePackageRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_1,
        )
        package_requirement_3 = SubPluginReleasePackageRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_2,
        )
        pypi_requirement_1 = SubPluginReleasePyPiRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_1,
        )
        pypi_requirement_2 = SubPluginReleasePyPiRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_1,
        )
        pypi_requirement_3 = SubPluginReleasePyPiRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_2,
        )
        vcs_requirement_1 = SubPluginReleaseVersionControlRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_1,
        )
        vcs_requirement_2 = SubPluginReleaseVersionControlRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_1,
        )
        vcs_requirement_3 = SubPluginReleaseVersionControlRequirementFactory(
            sub_plugin_release=cls.sub_plugin_release_2,
        )
        cls.regular_user = ForumUserFactory()
        cls.detail_api = 'api:sub-plugins:releases-detail'
        cls.list_api = 'api:sub-plugins:releases-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'sub_plugin_slug': cls.sub_plugin_1.slug,
                'version': cls.sub_plugin_release_1.version,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'sub_plugin_slug': cls.sub_plugin_1.slug,
            },
        )

        cls.payload_1 = {
            'notes': cls.sub_plugin_release_1.notes,
            'version': cls.sub_plugin_release_1.version,
            'created': {
                'actual': cls.sub_plugin_release_1.created.strftime(
                    '%Y-%m-%dT%H:%M:%S.%fZ',
                ),
                'locale': formats.date_format(
                    cls.sub_plugin_release_1.created,
                    'DATETIME_FORMAT',
                ),
                'locale_short': formats.date_format(
                    cls.sub_plugin_release_1.created,
                    'SHORT_DATETIME_FORMAT',
                ),
            },
            'created_by': {
                'forum_id': cls.sub_plugin_release_1.created_by.forum_id,
                'username': cls.sub_plugin_release_1.created_by.user.username,
            },
            'download_count': cls.sub_plugin_release_1.download_count,
            'download_requirements': [
                {
                    'url': download_requirement_1.download_requirement.url,
                    'optional': download_requirement_1.optional,
                },
                {
                    'url': download_requirement_2.download_requirement.url,
                    'optional': download_requirement_2.optional,
                },
            ],
            'package_requirements': [
                {
                    'name': package_requirement_1.package_requirement.name,
                    'slug': package_requirement_1.package_requirement.slug,
                    'version': package_requirement_1.version,
                    'optional': package_requirement_1.optional,
                },
                {
                    'name': package_requirement_2.package_requirement.name,
                    'slug': package_requirement_2.package_requirement.slug,
                    'version': package_requirement_2.version,
                    'optional': package_requirement_2.optional,
                },
            ],
            'pypi_requirements': [
                {
                    'name': pypi_requirement_1.pypi_requirement.name,
                    'slug': pypi_requirement_1.pypi_requirement.slug,
                    'version': pypi_requirement_1.version,
                    'optional': pypi_requirement_1.optional,
                },
                {
                    'name': pypi_requirement_2.pypi_requirement.name,
                    'slug': pypi_requirement_2.pypi_requirement.slug,
                    'version': pypi_requirement_2.version,
                    'optional': pypi_requirement_2.optional,
                },
            ],
            'vcs_requirements': [
                {
                    'url': vcs_requirement_1.vcs_requirement.url,
                    'version': vcs_requirement_1.version,
                    'optional': vcs_requirement_1.optional,
                },
                {
                    'url': vcs_requirement_2.vcs_requirement.url,
                    'version': vcs_requirement_2.version,
                    'optional': vcs_requirement_2.optional,
                },
            ],
        }
        cls.payload_2 = {
            'notes': cls.sub_plugin_release_2.notes,
            'version': cls.sub_plugin_release_2.version,
            'created': {
                'actual': cls.sub_plugin_release_2.created.strftime(
                    '%Y-%m-%dT%H:%M:%S.%fZ',
                ),
                'locale': formats.date_format(
                    cls.sub_plugin_release_2.created,
                    'DATETIME_FORMAT',
                ),
                'locale_short': formats.date_format(
                    cls.sub_plugin_release_2.created,
                    'SHORT_DATETIME_FORMAT',
                ),
            },
            'created_by': {
                'forum_id': cls.sub_plugin_release_2.created_by.forum_id,
                'username': cls.sub_plugin_release_2.created_by.user.username,
            },
            'download_count': cls.sub_plugin_release_2.download_count,
            'download_requirements': [
                {
                    'url': download_requirement_3.download_requirement.url,
                    'optional': download_requirement_3.optional,
                },
            ],
            'package_requirements': [
                {
                    'name': package_requirement_3.package_requirement.name,
                    'slug': package_requirement_3.package_requirement.slug,
                    'version': package_requirement_3.version,
                    'optional': package_requirement_3.optional,
                },
            ],
            'pypi_requirements': [
                {
                    'name': pypi_requirement_3.pypi_requirement.name,
                    'slug': pypi_requirement_3.pypi_requirement.slug,
                    'version': pypi_requirement_3.version,
                    'optional': pypi_requirement_3.optional,
                },
            ],
            'vcs_requirements': [
                {
                    'url': vcs_requirement_3.vcs_requirement.url,
                    'version': vcs_requirement_3.version,
                    'optional': vcs_requirement_3.optional,
                },
            ],
        }

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
            d2={'sub_plugin': {}, 'created_by': {'user': {}}},
        )
        prefetch_lookups = getattr(
            SubPluginReleaseViewSet.queryset,
            '_prefetch_related_lookups'
        )
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

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=SubPluginReleaseViewSet.http_method_names,
            tuple2=('get', 'post', 'options'),
        )

    @override_settings(DEBUG=True)
    def test_get_list(self):
        # Verify that a non-logged-in user can see results
        response = self.client.get(path=self.list_path)
        self.assertEqual(first=len(connection.queries), second=7)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        request = response.wsgi_request
        zip_file_base = f'{request.scheme}://{request.get_host()}'
        url_1 = self.sub_plugin_release_1.zip_file.url
        payload_1 = deepcopy(self.payload_1)
        payload_1['zip_file'] = f'{zip_file_base}{url_1}'
        url_2 = self.sub_plugin_release_2.zip_file.url
        payload_2 = deepcopy(self.payload_2)
        payload_2['zip_file'] = f'{zip_file_base}{url_2}'
        self.assertDictEqual(
            d1=content['results'][0],
            d2=payload_2,
        )
        self.assertDictEqual(
            d1=content['results'][1],
            d2=payload_1,
        )

        # Verify that regular user can see results
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.list_path)
        self.assertEqual(first=len(connection.queries), second=9)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2=payload_2,
        )
        self.assertDictEqual(
            d1=content['results'][1],
            d2=payload_1,
        )

        # Verify that contributors can see results
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.list_path)
        self.assertEqual(first=len(connection.queries), second=9)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2=payload_2,
        )
        self.assertDictEqual(
            d1=content['results'][1],
            d2=payload_1,
        )

        # Verify that the owner can see results
        self.client.force_login(self.owner.user)
        response = self.client.get(path=self.list_path)
        self.assertEqual(first=len(connection.queries), second=9)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2=payload_2,
        )
        self.assertDictEqual(
            d1=content['results'][1],
            d2=payload_1,
        )

    @override_settings(DEBUG=True)
    def test_get_list_empty(self):
        list_path = reverse(
            viewname=self.list_api,
            kwargs={
                'plugin_slug': self.plugin.slug,
                'sub_plugin_slug': self.sub_plugin_2.slug,
            },
        )

        # Verify that a non-logged-in user can see results
        response = self.client.get(path=list_path)
        self.assertEqual(first=len(connection.queries), second=2)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(first=response.json()['count'], second=0)

        # Verify that regular user can see results
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=list_path)
        self.assertEqual(first=len(connection.queries), second=4)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(first=response.json()['count'], second=0)

        # Verify that contributors can see results
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=list_path)
        self.assertEqual(first=len(connection.queries), second=4)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(first=response.json()['count'], second=0)

        # Verify that the owner can see results
        self.client.force_login(self.owner.user)
        response = self.client.get(path=list_path)
        self.assertEqual(first=len(connection.queries), second=4)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(first=response.json()['count'], second=0)

    @override_settings(DEBUG=True)
    def test_get_list_failure(self):
        response = self.client.get(
            path=reverse(
                viewname=self.list_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'sub_plugin_slug': 'invalid',
                },
            ),
        )
        self.assertEqual(first=len(connection.queries), second=1)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid sub_plugin_slug.'},
        )

    @override_settings(DEBUG=True)
    def test_get_details(self):
        environ = self.client._base_environ()
        zip_file_base = f'{environ["wsgi.url_scheme"]}://{environ["SERVER_NAME"]}'
        url_1 = self.sub_plugin_release_1.zip_file.url
        payload_1 = deepcopy(self.payload_1)
        payload_1['zip_file'] = f'{zip_file_base}{url_1}'
        url_2 = self.sub_plugin_release_2.zip_file.url
        payload_2 = deepcopy(self.payload_2)
        payload_2['zip_file'] = f'{zip_file_base}{url_2}'
        detail_path_2 = reverse(
            viewname=self.detail_api,
            kwargs={
                'plugin_slug': self.plugin.slug,
                'sub_plugin_slug': self.sub_plugin_1.slug,
                'version': self.sub_plugin_release_2.version,
            },
        )
        for path, payload in (
            (self.detail_path, payload_1),
            (detail_path_2, payload_2),
        ):
            # Verify that non-logged-in user can see details
            self.client.logout()
            response = self.client.get(path=path)
            self.assertEqual(first=len(connection.queries), second=6)
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
            response = self.client.get(path=path)
            self.assertEqual(first=len(connection.queries), second=8)
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
            response = self.client.get(path=path)
            self.assertEqual(first=len(connection.queries), second=8)
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
            response = self.client.get(path=path)
            self.assertEqual(first=len(connection.queries), second=8)
            self.assertEqual(
                first=response.status_code,
                second=status.HTTP_200_OK,
            )
            self.assertDictEqual(
                d1=response.json(),
                d2=payload,
            )

    @override_settings(DEBUG=True)
    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'sub_plugin_slug': self.sub_plugin_1.slug,
                    'version': '0.0.0',
                },
            ),
        )
        self.assertEqual(first=len(connection.queries), second=4)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Not found.'},
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post(self):
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'sub-plugins'
        file_path = base_path / 'test-plugin' / 'test-sub-plugin' / 'test-sub-plugin-v1.0.0.zip'

        # Verify that non-logged-in user cannot create a release
        version = '1.0.2'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=self.list_path,
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
        version = '1.0.2'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            self.client.force_login(self.regular_user.user)
            response = self.client.post(
                path=self.list_path,
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
        version = '1.0.2'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            self.client.force_login(self.contributor.user)
            response = self.client.post(
                path=self.list_path,
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
            first=self.sub_plugin_1.releases.count(),
            second=3,
        )
        content = response.json()
        release = self.sub_plugin_1.releases.get(version=content['version'])
        self.assertEqual(
            first=release.created_by.forum_id,
            second=self.contributor.forum_id,
        )
        self.assertEqual(
            first=release.version,
            second=version,
        )

        # Verify owner can create a release
        version = '1.0.3'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            self.client.force_login(self.owner.user)
            response = self.client.post(
                path=self.list_path,
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
            first=self.sub_plugin_1.releases.count(),
            second=4,
        )
        content = response.json()
        release = self.sub_plugin_1.releases.get(version=content['version'])
        self.assertEqual(
            first=release.created_by.forum_id,
            second=self.owner.forum_id,
        )
        self.assertEqual(
            first=release.version,
            second=version,
        )

        # Verify that the same version cannot be created twice
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=self.list_path,
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
        zip_basename = self.sub_plugin_1.basename
        sub_plugin = SubPluginFactory(
            plugin=self.plugin,
            owner=self.owner,
        )
        SubPluginReleaseFactory(
            sub_plugin=sub_plugin,
            version='1.0.0',
        )
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=reverse(
                    viewname=self.list_api,
                    kwargs={
                        'plugin_slug': self.plugin.slug,
                        'sub_plugin_slug': sub_plugin.slug,
                    },
                ),
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
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'sub-plugins'
        sub_plugin_file_path = base_path / 'test-plugin' / 'test-sub-plugin'
        file_path = sub_plugin_file_path / 'test-sub-plugin-requirements-v1.0.0.zip'
        version = '1.1.0'
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
            second=3,
        )
        self.assertEqual(
            first=PyPiRequirement.objects.count(),
            second=3,
        )
        self.assertEqual(
            first=VersionControlRequirement.objects.count(),
            second=3,
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
                path=self.list_path,
                data={
                    'version': version,
                    'zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )
        release = self.sub_plugin_1.releases.get(
            version=response.json()['version'],
        )
        self.assertEqual(
            first=DownloadRequirement.objects.count(),
            second=5,
        )
        self.assertEqual(
            first=release.download_requirements.count(),
            second=2,
        )
        self.assertEqual(
            first=PyPiRequirement.objects.count(),
            second=5,
        )
        self.assertEqual(
            first=release.pypi_requirements.count(),
            second=2,
        )
        self.assertEqual(
            first=VersionControlRequirement.objects.count(),
            second=5,
        )
        self.assertEqual(
            first=release.vcs_requirements.count(),
            second=2,
        )

    def test_options(self):
        # Verify that non-logged-in user cannot POST
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin_1} - Release',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot POST
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin_1} - Release',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can POST
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin_1} - Release',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'POST'})

        # Verify that the owner can POST
        self.client.force_login(user=self.owner.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin_1} - Release',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'POST'})

    def test_options_object(self):
        # Verify that non-logged-in user cannot DELETE/PATCH
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin_1} - Release',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot DELETE/PATCH
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin_1} - Release',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors cannot DELETE/PATCH
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin_1} - Release',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that the owner cannot DELETE/PATCH
        self.client.force_login(user=self.owner.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin_1} - Release',
        )
        self.assertNotIn(member='actions', container=content)
