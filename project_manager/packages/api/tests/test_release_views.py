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
from rest_framework.test import APITestCase

# App
from project_manager.common.api.views import ProjectReleaseViewSet
from project_manager.packages.api.serializers import PackageReleaseSerializer
from project_manager.packages.api.views import PackageReleaseViewSet
from project_manager.packages.models import (
    Package,
    PackageRelease,
    PackageReleaseDownloadRequirement,
    PackageReleasePackageRequirement,
    PackageReleasePyPiRequirement,
    PackageReleaseVersionControlRequirement,
)
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from test_utils.factories.packages import (
    PackageFactory,
    PackageContributorFactory,
    PackageReleaseFactory,
)
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PackageReleaseViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = package = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.package = PackageFactory(
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/packages/releases/'
        cls.api_path = f'{cls.base_api_path}{cls.package.slug}/'
        cls.contributor = ForumUserFactory()
        PackageContributorFactory(
            package=cls.package,
            user=cls.contributor,
        )
        cls.package_release = PackageReleaseFactory(
            package=cls.package,
            zip_file='release_v1.0.0.zip',
        )
        cls.regular_user = ForumUserFactory()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageReleaseViewSet, ProjectReleaseViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageReleaseViewSet.serializer_class,
            second=PackageReleaseSerializer,
        )
        self.assertEqual(
            first=PackageReleaseViewSet.project_type,
            second='package',
        )
        self.assertEqual(
            first=PackageReleaseViewSet.project_model,
            second=Package,
        )
        self.assertIs(
            expr1=PackageReleaseViewSet.queryset.model,
            expr2=PackageRelease,
        )
        self.assertDictEqual(
            d1=PackageReleaseViewSet.queryset.query.select_related,
            d2={'package': {}},
        )
        prefetch_lookups = PackageReleaseViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=4)

        lookup = prefetch_lookups[0]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='packagereleasepackagerequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PackageReleasePackageRequirement,
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
            second='packagereleasedownloadrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PackageReleaseDownloadRequirement,
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
            second='packagereleasepypirequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PackageReleasePyPiRequirement,
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
            second='packagereleaseversioncontrolrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PackageReleaseVersionControlRequirement,
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
            tuple1=PackageReleaseViewSet.http_method_names,
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
        timestamp = self.package_release.created
        request = response.wsgi_request
        zip_file = f'{request.scheme}://{request.get_host()}{self.package_release.zip_file.url}'
        created_by = self.package_release.created_by
        payload = {
            'notes': self.package_release.notes,
            'zip_file': zip_file,
            'version': self.package_release.version,
            'created': {
                'actual': timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'locale': formats.date_format(timestamp, 'DATETIME_FORMAT'),
                'locale_short': formats.date_format(timestamp, 'SHORT_DATETIME_FORMAT'),
            },
            'created_by': {
                'forum_id': created_by.forum_id,
                'username': created_by.user.username,
            },
            'download_count': self.package_release.download_count,
            'download_requirements': [],
            'package_requirements': [],
            'pypi_requirements': [],
            'vcs_requirements': [],
            'id': str(self.package_release.id),
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
        api_path = f'{self.api_path}{self.package_release.version}/'
        response = self.client.get(path=api_path)
        timestamp = self.package_release.created
        request = response.wsgi_request
        zip_file = f'{request.scheme}://{request.get_host()}{self.package_release.zip_file.url}'
        created_by = self.package_release.created_by
        payload = {
            'notes': self.package_release.notes,
            'zip_file': zip_file,
            'version': self.package_release.version,
            'created': {
                'actual': timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'locale': formats.date_format(timestamp, 'DATETIME_FORMAT'),
                'locale_short': formats.date_format(timestamp, 'SHORT_DATETIME_FORMAT'),
            },
            'created_by': {
                'forum_id': created_by.forum_id,
                'username': created_by.user.username,
            },
            'download_count': self.package_release.download_count,
            'download_requirements': [],
            'package_requirements': [],
            'pypi_requirements': [],
            'vcs_requirements': [],
            'id': str(self.package_release.id),
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
        api_path = f'{self.base_api_path}invalid/'
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid package_slug.'},
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post(self):
        package = PackageFactory(
            basename='test_package',
            owner=self.owner,
        )
        PackageReleaseFactory(
            package=package,
            version='1.0.0',
        )
        PackageContributorFactory(
            package=package,
            user=self.contributor,
        )
        api_path = f'{self.base_api_path}{package.slug}/'
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'packages'
        file_path = base_path / 'test-package' / 'test-package-v1.0.0.zip'

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

        # Verify that contributor can create a release
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
            first=package.releases.count(),
            second=2,
        )
        content = response.json()
        release = package.releases.get(id=content['id'])
        self.assertEqual(
            first=release.created_by.forum_id,
            second=self.contributor.forum_id,
        )
        self.assertEqual(
            first=release.version,
            second=version,
        )

        # Verify that owner can create a release
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
            first=package.releases.count(),
            second=3,
        )
        content = response.json()
        release = package.releases.get(id=content['id'])
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
        zip_basename = package.basename
        package = PackageFactory(
            owner=self.owner,
        )
        PackageReleaseFactory(
            package=package,
            version='1.0.0',
        )
        api_path = f'{self.base_api_path}{package.slug}/'
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
                    f" for package '{package.basename}'.",
                ],
            }
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post_with_requirements(self):
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'packages'
        file_path = base_path / 'test-package' / 'test-package-requirements-v1.0.0.zip'
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
        api_path = f'{self.base_api_path}{package.slug}/'
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
        release = PackageRelease.objects.get(pk=response.json()['id'])
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
            second=f'{self.package} - Release',
        )
