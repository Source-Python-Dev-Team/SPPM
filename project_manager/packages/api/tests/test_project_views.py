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
from project_manager.common.api.views import ProjectViewSet
from project_manager.packages.api.filtersets import PackageFilterSet
from project_manager.packages.api.serializers import (
    PackageCreateSerializer,
    PackageSerializer,
)
from project_manager.packages.api.views import PackageViewSet
from project_manager.packages.models import (
    Package,
    PackageRelease,
)
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from test_utils.factories.games import GameFactory
from test_utils.factories.packages import (
    PackageFactory,
    PackageContributorFactory,
    PackageGameFactory,
    PackageReleaseFactory,
    PackageTagFactory,
)
from test_utils.factories.tags import TagFactory
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PackageViewSetTestCase(APITestCase):

    contributor = owner = package = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.package = PackageFactory(
            owner=cls.owner,
            logo='logo.jpg',
        )
        cls.package_release = PackageReleaseFactory(
            package=cls.package,
            zip_file='/media/release_v1.0.0.zip',
        )
        cls.api_path = f'/api/packages/projects/'
        cls.contributor = ForumUserFactory()
        PackageContributorFactory(
            package=cls.package,
            user=cls.contributor,
        )
        cls.regular_user = ForumUserFactory()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PackageViewSet, ProjectViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageViewSet.filterset_class,
            second=PackageFilterSet,
        )
        self.assertEqual(
            first=PackageViewSet.serializer_class,
            second=PackageSerializer,
        )
        self.assertEqual(
            first=PackageViewSet.creation_serializer_class,
            second=PackageCreateSerializer,
        )
        self.assertIs(expr1=PackageViewSet.queryset.model, expr2=Package)
        prefetch_lookups = PackageViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=1)
        lookup = prefetch_lookups[0]
        self.assertEqual(first=lookup.prefetch_to, second='releases')
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('-created',),
        )
        self.assertDictEqual(
            d1=PackageViewSet.queryset.query.select_related,
            d2={'owner': {'user': {}}},
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PackageViewSet.http_method_names,
            tuple2=('get', 'post', 'patch', 'options'),
        )

    def test_get_list(self):
        # Verify that non logged in user can see results but not 'id'
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=1)
        request = response.wsgi_request
        domain = f'{request.scheme}://{request.get_host()}'
        zip_file = f'{domain}{self.package_release.get_absolute_url()}'
        logo = f'{domain}{self.package.logo.url}'
        created_timestamp = self.package.created
        updated_timestamp = self.package.updated
        payload = {
            'name': self.package.name,
            'slug': self.package.slug,
            'total_downloads': self.package.total_downloads,
            'current_release': {
                'version': self.package_release.version,
                'notes': self.package_release.notes,
                'zip_file': zip_file,
            },
            'created': {
                'actual': created_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'locale': formats.date_format(created_timestamp, 'DATETIME_FORMAT'),
                'locale_short': formats.date_format(created_timestamp, 'SHORT_DATETIME_FORMAT'),
            },
            'updated': {
                'actual': updated_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'locale': formats.date_format(updated_timestamp, 'DATETIME_FORMAT'),
                'locale_short': formats.date_format(updated_timestamp, 'SHORT_DATETIME_FORMAT'),
            },
            'synopsis': self.package.synopsis,
            'description': self.package.description,
            'configuration': self.package.configuration,
            'logo': logo,
            'video': self.package.video,
            'owner': {
                'forum_id': self.package.owner.forum_id,
                'username': self.package.owner.user.username,
            }
        }
        self.assertDictEqual(
            d1=content['results'][0],
            d2=payload,
        )

        # Verify that regular user can see results but not 'id'
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

        # Verify that contributors can see results AND 'id'
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

        # Verify that the owner can see results AND 'id'
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

    def test_get_list_filters(self):
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=1,
        )

        # Validate tag filtering
        response = self.client.get(path=f'{self.api_path}?tag=test_tag')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=0,
        )
        tag = TagFactory(name='test_tag')
        PackageTagFactory(
            package=self.package,
            tag=tag,
        )
        response = self.client.get(path=f'{self.api_path}?tag=test_tag')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=1,
        )

        # Validate game filtering
        response = self.client.get(path=f'{self.api_path}?game=game1')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=0,
        )
        game = GameFactory(
            name='Game1',
            basename='game1',
            icon='icon1.jpg',
        )
        PackageGameFactory(
            package=self.package,
            game=game,
        )
        response = self.client.get(path=f'{self.api_path}?game=game1')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=1,
        )

        # Validate game filtering
        response = self.client.get(
            path=f'{self.api_path}?user={self.regular_user.user.username}',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=0,
        )
        response = self.client.get(
            path=f'{self.api_path}?user={self.contributor.user.username}',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=1,
        )
        response = self.client.get(
            path=f'{self.api_path}?user={self.owner.user.username}',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=1,
        )

    def test_get_details(self):
        # Verify that non logged in user can see details
        api_path = f'{self.api_path}{self.package.slug}/'
        response = self.client.get(path=api_path)
        request = response.wsgi_request
        domain = f'{request.scheme}://{request.get_host()}'
        zip_file = f'{domain}{self.package_release.get_absolute_url()}'
        logo = f'{domain}{self.package.logo.url}'
        created_timestamp = self.package.created
        updated_timestamp = self.package.updated
        payload = {
            'name': self.package.name,
            'slug': self.package.slug,
            'total_downloads': self.package.total_downloads,
            'current_release': {
                'version': self.package_release.version,
                'notes': self.package_release.notes,
                'zip_file': zip_file,
                'package_requirements': [],
                'pypi_requirements': [],
                'version_control_requirements': [],
                'download_requirements': [],
            },
            'created': {
                'actual': created_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'locale': formats.date_format(created_timestamp, 'DATETIME_FORMAT'),
                'locale_short': formats.date_format(created_timestamp, 'SHORT_DATETIME_FORMAT'),
            },
            'updated': {
                'actual': updated_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'locale': formats.date_format(updated_timestamp, 'DATETIME_FORMAT'),
                'locale_short': formats.date_format(updated_timestamp, 'SHORT_DATETIME_FORMAT'),
            },
            'synopsis': self.package.synopsis,
            'description': self.package.description,
            'configuration': self.package.configuration,
            'logo': logo,
            'video': self.package.video,
            'owner': {
                'forum_id': self.package.owner.forum_id,
                'username': self.package.owner.user.username,
            }
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

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post(self):
        # Verify non logged in user cannot create a package
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'packages'
        file_path = base_path / 'test-package' / 'test-package-v1.0.0.zip'
        version = '1.0.0'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=self.api_path,
                data={
                    'name': 'Test Package',
                    'releases.notes': '',
                    'releases.version': version,
                    'releases.zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that a logged in user can create a package
        self.assertEqual(
            first=Package.objects.count(),
            second=1,
        )
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            self.client.force_login(self.regular_user.user)
            response = self.client.post(
                path=self.api_path,
                data={
                    'name': 'Test Package',
                    'releases.notes': '',
                    'releases.version': version,
                    'releases.zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )
        self.assertEqual(
            first=Package.objects.count(),
            second=2,
        )
        content = response.json()
        package = Package.objects.get(slug=content['slug'])
        self.assertEqual(
            first=package.releases.count(),
            second=1,
        )
        release = package.releases.get()
        self.assertEqual(
            first=release.created_by.forum_id,
            second=self.regular_user.forum_id,
        )
        self.assertEqual(
            first=release.version,
            second=version,
        )

        # Verify cannot create a package where the basename already exists
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=self.api_path,
                data={
                    'name': 'Test Package',
                    'releases.notes': '',
                    'releases.version': version,
                    'releases.zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'basename': 'Package already exists. Cannot create.'}
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post_with_requirements(self):
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'packages'
        file_path = base_path / 'test-package' / 'test-package-requirements-v1.0.0.zip'
        version = '1.0.0'
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
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=self.api_path,
                data={
                    'name': 'Test Package',
                    'releases.notes': '',
                    'releases.version': version,
                    'releases.zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )
        contents = response.json()
        package = Package.objects.get(slug=contents['slug'])
        release = PackageRelease.objects.get(package=package)
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

    def test_patch(self):
        # Verify that non logged in user cannot update the package
        api_path = f'{self.api_path}{self.package.slug}/'
        response = self.client.patch(
            path=api_path,
            data={
                'synopsis': 'Test Synopsis',
            }
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot update the package
        self.client.force_login(self.regular_user.user)
        response = self.client.patch(
            path=api_path,
            data={
                'synopsis': 'Test Synopsis',
            }
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can update the package
        self.client.force_login(self.contributor.user)
        response = self.client.patch(
            path=api_path,
            data={
                'synopsis': 'Test Synopsis',
            }
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )

        # Verify that owner can update the package
        self.client.force_login(self.owner.user)
        response = self.client.patch(
            path=api_path,
            data={
                'synopsis': 'New Test Synopsis',
            }
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second='Package List',
        )
