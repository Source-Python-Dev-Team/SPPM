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
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.api.common.views import ProjectViewSet
from project_manager.sub_plugins.api.filtersets import SubPluginFilterSet
from project_manager.sub_plugins.api.serializers import (
    SubPluginCreateSerializer,
    SubPluginSerializer,
)
from project_manager.sub_plugins.api.views import SubPluginViewSet
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginRelease,
)
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from test_utils.factories.games import GameFactory
from test_utils.factories.packages import PackageFactory, PackageReleaseFactory
from test_utils.factories.plugins import PluginFactory, SubPluginPathFactory
from test_utils.factories.sub_plugins import (
    SubPluginContributorFactory,
    SubPluginFactory,
    SubPluginGameFactory,
    SubPluginReleaseFactory,
    SubPluginTagFactory,
)
from test_utils.factories.tags import TagFactory
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginViewSetTestCase(APITestCase):

    contributor = list_api = owner = sub_plugin = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        plugin = PluginFactory()
        cls.sub_plugin = SubPluginFactory(
            owner=cls.owner,
            plugin=plugin,
            logo='logo.jpg',
        )
        cls.sub_plugin_release = SubPluginReleaseFactory(
            sub_plugin=cls.sub_plugin,
            zip_file='/media/release_v1.0.0.zip',
        )
        cls.list_api = 'api:sub-plugins:projects-list'
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={'plugin_slug': plugin.slug},
        )
        cls.detail_path = reverse(
            viewname='api:sub-plugins:projects-detail',
            kwargs={
                'plugin_slug': plugin.slug,
                'slug': cls.sub_plugin.slug,
            }
        )
        cls.contributor = ForumUserFactory()
        SubPluginContributorFactory(
            sub_plugin=cls.sub_plugin,
            user=cls.contributor,
        )
        cls.regular_user = ForumUserFactory()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginViewSet, ProjectViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginViewSet.filterset_class,
            second=SubPluginFilterSet,
        )
        self.assertEqual(
            first=SubPluginViewSet.serializer_class,
            second=SubPluginSerializer,
        )
        self.assertEqual(
            first=SubPluginViewSet.creation_serializer_class,
            second=SubPluginCreateSerializer,
        )
        self.assertIs(expr1=SubPluginViewSet.queryset.model, expr2=SubPlugin)
        prefetch_lookups = SubPluginViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=1)
        lookup = prefetch_lookups[0]
        self.assertEqual(first=lookup.prefetch_to, second='releases')
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('-created',),
        )
        self.assertDictEqual(
            d1=SubPluginViewSet.queryset.query.select_related,
            d2={'owner': {'user': {}}, 'plugin': {}},
        )

    def test_get_queryset(self):
        with self.assertRaises(ParseError) as context:
            obj = SubPluginViewSet()
            obj.kwargs = {}
            obj.get_queryset()

        self.assertEqual(
            first=context.exception.detail,
            second='Invalid plugin_slug.',
        )

        # TODO: validate the query returns the correct data
        plugin = PluginFactory()
        obj.kwargs = {'plugin_slug': plugin.slug}
        obj.get_queryset()

        # TODO: validate the query returns the correct data
        obj.kwargs = {}
        obj.plugin = plugin
        obj.get_queryset()

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=SubPluginViewSet.http_method_names,
            tuple2=('get', 'post', 'patch', 'options'),
        )

    def test_get_list(self):
        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=self.list_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        request = response.wsgi_request
        domain = f'{request.scheme}://{request.get_host()}'
        zip_file = f'{domain}{self.sub_plugin_release.get_absolute_url()}'
        logo = f'{domain}{self.sub_plugin.logo.url}'
        self.assertEqual(first=content['count'], second=1)
        created_timestamp = self.sub_plugin.created
        updated_timestamp = self.sub_plugin.updated
        payload = {
            'name': self.sub_plugin.name,
            'slug': self.sub_plugin.slug,
            'total_downloads': self.sub_plugin.total_downloads,
            'current_release': {
                'version': self.sub_plugin_release.version,
                'notes': self.sub_plugin_release.notes,
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
            'synopsis': self.sub_plugin.synopsis,
            'description': self.sub_plugin.description,
            'configuration': self.sub_plugin.configuration,
            'logo': logo,
            'video': self.sub_plugin.video,
            'owner': {
                'forum_id': self.sub_plugin.owner.forum_id,
                'username': self.sub_plugin.owner.user.username,
            }
        }
        self.assertDictEqual(
            d1=content['results'][0],
            d2=payload,
        )

        # Verify that regular user can see results but not 'id'
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=1,
        )

        # Validate tag filtering
        response = self.client.get(
            path=self.list_path,
            data={'tag': 'test_tag'},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=0,
        )
        tag = TagFactory(name='test_tag')
        SubPluginTagFactory(
            sub_plugin=self.sub_plugin,
            tag=tag,
        )
        response = self.client.get(
            path=self.list_path,
            data={'tag': 'test_tag'},
        )
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
        SubPluginGameFactory(
            sub_plugin=self.sub_plugin,
            game=game,
        )
        response = self.client.get(
            path=self.list_path,
            data={'game': 'game1'},
        )
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
            data={'user': self.contributor.user.username},
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
            path=self.list_path,
            data={'user': self.owner.user.username},
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
        # Verify that non-logged-in user can see details
        response = self.client.get(path=self.detail_path)
        request = response.wsgi_request
        domain = f'{request.scheme}://{request.get_host()}'
        zip_file = f'{domain}{self.sub_plugin_release.get_absolute_url()}'
        logo = f'{domain}{self.sub_plugin.logo.url}'
        created_timestamp = self.sub_plugin.created
        updated_timestamp = self.sub_plugin.updated
        payload = {
            'name': self.sub_plugin.name,
            'slug': self.sub_plugin.slug,
            'total_downloads': self.sub_plugin.total_downloads,
            'current_release': {
                'version': self.sub_plugin_release.version,
                'notes': self.sub_plugin_release.notes,
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
            'synopsis': self.sub_plugin.synopsis,
            'description': self.sub_plugin.description,
            'configuration': self.sub_plugin.configuration,
            'logo': logo,
            'video': self.sub_plugin.video,
            'owner': {
                'forum_id': self.sub_plugin.owner.forum_id,
                'username': self.sub_plugin.owner.user.username,
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
        response = self.client.get(path=self.detail_path)
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
        response = self.client.get(path=self.detail_path)
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
        response = self.client.get(path=self.detail_path)
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
        # Verify non-logged-in user cannot create a sub-plugin
        plugin = PluginFactory(
            basename='test_plugin',
        )
        SubPluginPathFactory(
            plugin=plugin,
            path='sub_plugins',
            allow_package_using_basename=True,
        )
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'sub-plugins'
        file_path = base_path / 'test-plugin' / 'test-sub-plugin' / 'test-sub-plugin-v1.0.0.zip'
        version = '1.0.0'
        api_path = reverse(
            viewname=self.list_api,
            kwargs={'plugin_slug': plugin.slug},
        )
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=api_path,
                data={
                    'name': 'Test SubPlugin',
                    'releases.notes': '',
                    'releases.version': version,
                    'releases.zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that a logged-in user can create a sub-plugin
        self.assertEqual(
            first=SubPlugin.objects.count(),
            second=1,
        )
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            self.client.force_login(self.regular_user.user)
            response = self.client.post(
                path=api_path,
                data={
                    'name': 'Test SubPlugin',
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
            first=SubPlugin.objects.count(),
            second=2,
        )
        content = response.json()
        sub_plugin = SubPlugin.objects.get(slug=content['slug'])
        self.assertEqual(
            first=sub_plugin.releases.count(),
            second=1,
        )
        release = sub_plugin.releases.get()
        self.assertEqual(
            first=release.created_by.forum_id,
            second=self.regular_user.forum_id,
        )
        self.assertEqual(
            first=release.version,
            second=version,
        )

        # Verify cannot create a sub-plugin where the basename already exists
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=api_path,
                data={
                    'name': 'Test SubPlugin',
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
            d2={'basename': 'SubPlugin already exists. Cannot create.'}
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
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'sub-plugins'
        file_path = base_path / 'test-plugin' / 'test-sub-plugin' / 'test-sub-plugin-requirements-v1.0.0.zip'
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
                path=reverse(
                    viewname=self.list_api,
                    kwargs={'plugin_slug': plugin.slug},
                ),
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
        sub_plugin = SubPlugin.objects.get(slug=contents['slug'], plugin=plugin)
        release = SubPluginRelease.objects.get(sub_plugin=sub_plugin)
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
        # Verify that non-logged-in user cannot update a path
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

        # Verify that regular user cannot update a path
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

        # Verify that contributor can update a path
        self.client.force_login(self.contributor.user)
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

        # Verify that owner can update a path
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
            second='Sub Plugin List',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user can POST
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second='Sub Plugin List',
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
            second='Sub Plugin Instance',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot PATCH
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second='Sub Plugin Instance',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can PATCH
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second='Sub Plugin Instance',
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
            second='Sub Plugin Instance',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'PATCH'})
