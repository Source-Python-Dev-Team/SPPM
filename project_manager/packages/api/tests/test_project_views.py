# =============================================================================
# IMPORTS
# =============================================================================
# Python
import shutil
import tempfile
from copy import deepcopy
from datetime import timedelta

# Django
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import connection
from django.test import override_settings
from django.utils import formats
from django.utils.timezone import now

# Third Party Python
from path import Path

# Third Party Django
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.api.common.views import ProjectViewSet
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
from users.models import ForumUser


# =============================================================================
# TEST CASES
# =============================================================================
class PackageViewSetTestCase(APITestCase):

    contributor_1 = contributor_2 = current_release_1 = None
    current_release_2 = detail_api = owner = package_1 = package_2 = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.package_1 = PackageFactory(
            owner=cls.owner,
            logo='logo.jpg',
            created=now() - timedelta(minutes=2),
            updated=now() - timedelta(minutes=2),
        )
        cls.package_2 = PackageFactory(
            owner=cls.owner,
            created=now() - timedelta(minutes=1),
            updated=now() - timedelta(minutes=1),
        )
        PackageReleaseFactory(
            package=cls.package_1,
            zip_file='/media/release_v1.0.0.zip',
        )
        cls.current_release_1 = PackageReleaseFactory(
            package=cls.package_1,
            zip_file='/media/release_v1.0.1.zip',
        )
        cls.current_release_2 = PackageReleaseFactory(
            package=cls.package_2,
            zip_file='/media/release_v1.0.0.zip',
        )
        cls.list_path = reverse(
            viewname='api:packages:projects-list',
        )
        cls.detail_api = 'api:packages:projects-detail'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'pk': cls.package_1.slug,
            }
        )
        cls.contributor_1 = ForumUserFactory()
        cls.contributor_2 = ForumUserFactory()
        PackageContributorFactory(
            package=cls.package_1,
            user=cls.contributor_1,
        )
        PackageContributorFactory(
            package=cls.package_1,
            user=cls.contributor_2,
        )
        cls.regular_user = ForumUserFactory()

        cls.payload_1 = {
            'name': cls.package_1.name,
            'slug': cls.package_1.slug,
            'total_downloads': cls.package_1.total_downloads,
            'current_release': {
                'version': cls.current_release_1.version,
                'notes': cls.current_release_1.notes,
            },
            'created': {
                'actual': cls.package_1.created.strftime(
                    '%Y-%m-%dT%H:%M:%S.%fZ',
                ),
                'locale': formats.date_format(
                    cls.package_1.created,
                    'DATETIME_FORMAT',
                ),
                'locale_short': formats.date_format(
                    cls.package_1.created,
                    'SHORT_DATETIME_FORMAT',
                ),
            },
            'updated': {
                'actual': cls.package_1.updated.strftime(
                    '%Y-%m-%dT%H:%M:%S.%fZ',
                ),
                'locale': formats.date_format(
                    cls.package_1.updated,
                    'DATETIME_FORMAT',
                ),
                'locale_short': formats.date_format(
                    cls.package_1.updated,
                    'SHORT_DATETIME_FORMAT',
                ),
            },
            'synopsis': cls.package_1.synopsis,
            'description': cls.package_1.description,
            'configuration': cls.package_1.configuration,
            'video': cls.package_1.video,
            'owner': {
                'forum_id': cls.package_1.owner.forum_id,
                'username': cls.package_1.owner.user.username,
            },
            'contributors': [
                {
                    'forum_id': cls.contributor_1.forum_id,
                    'username': cls.contributor_1.user.username,
                },
                {
                    'forum_id': cls.contributor_2.forum_id,
                    'username': cls.contributor_2.user.username,
                },
            ],
        }
        cls.payload_2 = {
            'name': cls.package_2.name,
            'slug': cls.package_2.slug,
            'total_downloads': cls.package_2.total_downloads,
            'current_release': {
                'version': cls.current_release_2.version,
                'notes': cls.current_release_2.notes,
            },
            'created': {
                'actual': cls.package_2.created.strftime(
                    '%Y-%m-%dT%H:%M:%S.%fZ',
                ),
                'locale': formats.date_format(
                    cls.package_2.created,
                    'DATETIME_FORMAT',
                ),
                'locale_short': formats.date_format(
                    cls.package_2.created,
                    'SHORT_DATETIME_FORMAT',
                ),
            },
            'updated': {
                'actual': cls.package_2.updated.strftime(
                    '%Y-%m-%dT%H:%M:%S.%fZ',
                ),
                'locale': formats.date_format(
                    cls.package_2.updated,
                    'DATETIME_FORMAT',
                ),
                'locale_short': formats.date_format(
                    cls.package_2.updated,
                    'SHORT_DATETIME_FORMAT',
                ),
            },
            'synopsis': cls.package_2.synopsis,
            'description': cls.package_2.description,
            'configuration': cls.package_2.configuration,
            'logo': None,
            'video': cls.package_2.video,
            'owner': {
                'forum_id': cls.package_2.owner.forum_id,
                'username': cls.package_2.owner.user.username,
            },
            'contributors': [],
        }

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
        prefetch_lookups = getattr(
            PackageViewSet.queryset,
            '_prefetch_related_lookups'
        )
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

    def test_get_queryset(self):
        obj = PackageViewSet()
        setattr(obj, 'action', 'retrieve')
        prefetch_lookups = getattr(
            obj.get_queryset(),
            '_prefetch_related_lookups'
        )
        self.assertEqual(first=len(prefetch_lookups), second=1)

        setattr(obj, 'action', 'list')
        prefetch_lookups = getattr(
            obj.get_queryset(),
            '_prefetch_related_lookups'
        )
        self.assertEqual(first=len(prefetch_lookups), second=2)
        lookup = prefetch_lookups[1]
        self.assertEqual(first=lookup.prefetch_to, second='contributors')
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=ForumUser,
        )
        self.assertEqual(
            first=lookup.queryset.query.select_related,
            second={'user': {}}
        )

    @override_settings(DEBUG=True)
    def test_get_list(self):
        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=self.list_path)
        self.assertEqual(first=len(connection.queries), second=4)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        request = response.wsgi_request
        domain = f'{request.scheme}://{request.get_host()}'
        zip_file_1 = f'{domain}{self.current_release_1.get_absolute_url()}'
        payload_1 = deepcopy(self.payload_1)
        payload_1['current_release']['zip_file'] = zip_file_1
        payload_1['logo'] = f'{domain}{self.package_1.logo.url}'
        zip_file_2 = f'{domain}{self.current_release_2.get_absolute_url()}'
        payload_2 = deepcopy(self.payload_2)
        payload_2['current_release']['zip_file'] = zip_file_2
        self.assertDictEqual(
            d1=content['results'][0],
            d2=payload_2,
        )
        self.assertDictEqual(
            d1=content['results'][1],
            d2=payload_1,
        )

        # Verify that regular user can see results but not 'id'
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.list_path)
        self.assertEqual(first=len(connection.queries), second=6)
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

        # Verify that contributors can see results AND 'id'
        self.client.force_login(self.contributor_1.user)
        response = self.client.get(path=self.list_path)
        self.assertEqual(first=len(connection.queries), second=6)
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

        # Verify that the owner can see results AND 'id'
        self.client.force_login(self.owner.user)
        response = self.client.get(path=self.list_path)
        self.assertEqual(first=len(connection.queries), second=6)
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
    def test_get_list_filters(self):
        response = self.client.get(path=self.list_path)
        self.assertEqual(first=len(connection.queries), second=4)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=2,
        )

        # Validate tag filtering
        response = self.client.get(
            path=self.list_path,
            data={'tag': 'test_tag'},
        )
        self.assertEqual(first=len(connection.queries), second=1)
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
            package=self.package_1,
            tag=tag,
        )
        response = self.client.get(
            path=self.list_path,
            data={'tag': 'test_tag'},
        )
        self.assertEqual(first=len(connection.queries), second=4)
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
            path=self.list_path,
            data={'game': 'game1'},
        )
        self.assertEqual(first=len(connection.queries), second=1)
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
            package=self.package_1,
            game=game,
        )
        response = self.client.get(
            path=self.list_path,
            data={'game': 'game1'},
        )
        self.assertEqual(first=len(connection.queries), second=4)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=1,
        )

        # Validate user filtering
        response = self.client.get(
            path=self.list_path,
            data={'user': self.regular_user.user.username},
        )
        self.assertEqual(first=len(connection.queries), second=1)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=0,
        )
        response = self.client.get(
            path=self.list_path,
            data={'user': self.contributor_1.user.username},
        )
        self.assertEqual(first=len(connection.queries), second=4)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=1,
        )
        response = self.client.get(
            path=self.list_path,
            data={'user': self.owner.user.username},
        )
        self.assertEqual(first=len(connection.queries), second=4)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=2,
        )

    @override_settings(DEBUG=True)
    def test_get_details(self):
        environ = getattr(self.client, '_base_environ')()
        domain = f'{environ["wsgi.url_scheme"]}://{environ["SERVER_NAME"]}'
        zip_file_1 = f'{domain}{self.current_release_1.get_absolute_url()}'
        payload_1 = deepcopy(self.payload_1)
        payload_1['current_release']['zip_file'] = zip_file_1
        payload_1['current_release']['download_requirements'] = []
        payload_1['current_release']['package_requirements'] = []
        payload_1['current_release']['pypi_requirements'] = []
        payload_1['current_release']['version_control_requirements'] = []
        payload_1['logo'] = f'{domain}{self.package_1.logo.url}'
        del payload_1['contributors']
        zip_file_2 = f'{domain}{self.current_release_2.get_absolute_url()}'
        payload_2 = deepcopy(self.payload_2)
        payload_2['current_release']['zip_file'] = zip_file_2
        payload_2['current_release']['download_requirements'] = []
        payload_2['current_release']['package_requirements'] = []
        payload_2['current_release']['pypi_requirements'] = []
        payload_2['current_release']['version_control_requirements'] = []
        del payload_2['contributors']
        detail_path_2 = reverse(
            viewname=self.detail_api,
            kwargs={
                'pk': self.package_2.slug,
            }
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
            self.client.force_login(self.contributor_1.user)
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

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post(self):
        # Verify non-logged-in user cannot create a package
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'packages'
        file_path = base_path / 'test-package' / 'test-package-v1.0.0.zip'
        version = '1.0.0'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=self.list_path,
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

        # Verify that a logged-in user can create a package
        self.assertEqual(
            first=Package.objects.count(),
            second=2,
        )
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            self.client.force_login(self.regular_user.user)
            response = self.client.post(
                path=self.list_path,
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
            second=3,
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
                path=self.list_path,
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
                path=self.list_path,
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
        # Verify that non-logged-in user cannot update the package
        response = self.client.patch(
            path=self.detail_path,
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
            path=self.detail_path,
            data={
                'synopsis': 'Test Synopsis',
            }
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can update the package
        self.client.force_login(self.contributor_1.user)
        response = self.client.patch(
            path=self.detail_path,
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
            path=self.detail_path,
            data={
                'synopsis': 'New Test Synopsis',
            }
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )

    def test_options(self):
        # Verify that non-logged-in user cannot POST
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second='Package List',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user can POST
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second='Package List',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'POST'})

    def test_options_object(self):
        # Verify that non-logged-in user cannot PATCH
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second='Package Instance',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot PATCH
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second='Package Instance',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can PATCH
        self.client.force_login(user=self.contributor_1.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second='Package Instance',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'PATCH'})

        # Verify that the owner can PATCH
        self.client.force_login(user=self.owner.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second='Package Instance',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'PATCH'})
