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
from PIL import Image
from rest_framework import status
from rest_framework.parsers import ParseError
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.common.api.views import (
    ProjectAPIView,
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectReleaseViewSet,
    ProjectTagViewSet,
    ProjectViewSet,
)
from project_manager.sub_plugins.api.filtersets import SubPluginFilterSet
from project_manager.sub_plugins.api.serializers import (
    SubPluginContributorSerializer,
    SubPluginCreateSerializer,
    SubPluginGameSerializer,
    SubPluginImageSerializer,
    SubPluginReleaseSerializer,
    SubPluginSerializer,
    SubPluginTagSerializer,
)
from project_manager.sub_plugins.api.views import (
    SubPluginAPIView,
    SubPluginContributorViewSet,
    SubPluginGameViewSet,
    SubPluginImageViewSet,
    SubPluginReleaseViewSet,
    SubPluginTagViewSet,
    SubPluginViewSet,
)
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
from test_utils.factories.games import GameFactory
from test_utils.factories.plugins import PluginFactory, SubPluginPathFactory
from test_utils.factories.sub_plugins import (
    SubPluginContributorFactory,
    SubPluginFactory,
    SubPluginGameFactory,
    SubPluginImageFactory,
    SubPluginReleaseFactory,
    SubPluginTagFactory,
)
from test_utils.factories.tags import TagFactory
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginAPIViewTestCase(APITestCase):

    api_path = '/api/sub-plugins/'

    def test_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginAPIView, ProjectAPIView))

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginAPIView.project_type,
            second='sub-plugin',
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=SubPluginAPIView.http_method_names,
            tuple2=('get', 'options'),
        )

    def test_get(self):
        response = self.client.get(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        base_path = reverse(
            viewname=f'api:sub-plugins:endpoints',
            request=response.wsgi_request,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'contributors': base_path + f'contributors/<plugin>/<sub-plugin>/',
                'games': base_path + f'games/<plugin>/<sub-plugin>/',
                'images': base_path + f'images/<plugin>/<sub-plugin>/',
                'projects': base_path + f'projects/<plugin>/',
                'releases': base_path + f'releases/<plugin>/<sub-plugin>/',
                'tags': base_path + f'tags/<plugin>/<sub-plugin>/',
            }
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(first=response.json()['name'], second='Sub-Plugin APIs')


class SubPluginContributorViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = plugin = sub_plugin = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory()
        cls.sub_plugin = SubPluginFactory(
            plugin=cls.plugin,
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/sub-plugins/contributors/{cls.plugin.slug}/'
        cls.api_path = f'{cls.base_api_path}{cls.sub_plugin.slug}/'
        cls.contributor = ForumUserFactory()
        cls.sub_plugin_contributor = SubPluginContributorFactory(
            sub_plugin=cls.sub_plugin,
            user=cls.contributor,
        )
        cls.new_contributor = ForumUserFactory()
        cls.regular_user = ForumUserFactory()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                SubPluginContributorViewSet,
                ProjectContributorViewSet,
            ),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginContributorViewSet.serializer_class,
            second=SubPluginContributorSerializer,
        )
        self.assertEqual(
            first=SubPluginContributorViewSet.project_type,
            second='sub-plugin',
        )
        self.assertEqual(
            first=SubPluginContributorViewSet.project_model,
            second=SubPlugin,
        )
        self.assertIs(
            expr1=SubPluginContributorViewSet.queryset.model,
            expr2=SubPluginContributor,
        )
        self.assertDictEqual(
            d1=SubPluginContributorViewSet.queryset.query.select_related,
            d2={'user': {'user': {}}, 'sub_plugin': {}}
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=SubPluginContributorViewSet.http_method_names,
            tuple2=('get', 'post', 'delete', 'options'),
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
        user = self.contributor
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'user': {
                    'forum_id': user.forum_id,
                    'username': user.user.username,
                },
            },
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
        user = self.contributor
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'user': {
                    'forum_id': user.forum_id,
                    'username': user.user.username,
                },
            },
        )

        # Verify that contributors can see results but not 'id'
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
            d2={
                'user': {
                    'forum_id': user.forum_id,
                    'username': user.user.username,
                },
            },
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
            d2={
                'user': {
                    'forum_id': user.forum_id,
                    'username': user.user.username,
                },
                'id': str(self.sub_plugin_contributor.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.sub_plugin_contributor.id}/'
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot see details
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributors cannot see details
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
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
            d2={
                'user': {
                    'forum_id': self.sub_plugin_contributor.user.forum_id,
                    'username': self.sub_plugin_contributor.user.user.username,
                },
                'id': str(self.sub_plugin_contributor.id),
            },
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
            d2={'detail': 'Invalid sub_plugin_slug.'},
        )

    def test_post(self):
        # Verify that non logged in user cannot add a contributor
        response = self.client.post(
            path=self.api_path,
            data={'username': self.new_contributor.user.username},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot add a contributor
        self.client.force_login(self.regular_user.user)
        response = self.client.post(
            path=self.api_path,
            data={'username': self.new_contributor.user.username},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor cannot add a contributor
        self.client.force_login(self.contributor.user)
        response = self.client.post(
            path=self.api_path,
            data={'username': self.new_contributor.user.username},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that owner can add a contributor
        self.client.force_login(self.owner.user)
        response = self.client.post(
            path=self.api_path,
            data={'username': self.new_contributor.user.username},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

    def test_post_failure(self):
        self.client.force_login(self.owner.user)

        # Verify existing contributor cannot be added
        response = self.client.post(
            path=self.api_path,
            data={'username': self.contributor.user.username},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'username': [f'User {self.contributor.user.username} is already a contributor']},
        )

        # Verify owner cannot be added
        response = self.client.post(
            path=self.api_path,
            data={'username': self.owner.user.username},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'username': [f'User {self.owner.user.username} is the owner, cannot add as a contributor']},
        )

        # Verify unknown username cannot be added
        invalid_username = 'invalid'
        response = self.client.post(
            path=self.api_path,
            data={'username': invalid_username},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'username': [f'No user named "{invalid_username}".']},
        )

    def test_delete(self):
        # Verify that non logged in user cannot delete a contributor
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_contributor.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a contributor
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_contributor.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor cannot delete a contributor
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_contributor.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that owner can delete a contributor
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_contributor.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second=f'{self.sub_plugin} - Contributor',
        )


class SubPluginGameViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = game_1 = game_2 = plugin = sub_plugin = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory()
        cls.sub_plugin = SubPluginFactory(
            owner=cls.owner,
            plugin=cls.plugin,
        )
        cls.base_api_path = f'/api/sub-plugins/games/{cls.plugin.slug}/'
        cls.api_path = f'{cls.base_api_path}{cls.sub_plugin.slug}/'
        cls.contributor = ForumUserFactory()
        cls.package_contributor = SubPluginContributorFactory(
            sub_plugin=cls.sub_plugin,
            user=cls.contributor,
        )
        cls.game_1 = GameFactory(
            name='Game1',
            basename='game1',
            icon='icon1.jpg',
        )
        cls.game_2 = GameFactory(
            name='Game2',
            basename='game2',
            icon='icon2.jpg',
        )
        cls.game_3 = GameFactory(
            name='Game3',
            basename='game3',
            icon='icon3.jpg',
        )
        cls.game_4 = GameFactory(
            name='Game4',
            basename='game4',
            icon='icon4.jpg',
        )
        cls.sub_plugin_game_1 = SubPluginGameFactory(
            sub_plugin=cls.sub_plugin,
            game=cls.game_1,
        )
        cls.sub_plugin_game_2 = SubPluginGameFactory(
            sub_plugin=cls.sub_plugin,
            game=cls.game_2,
        )
        cls.regular_user = ForumUserFactory()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginGameViewSet, ProjectGameViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginGameViewSet.serializer_class,
            second=SubPluginGameSerializer,
        )
        self.assertEqual(
            first=SubPluginGameViewSet.project_type,
            second='sub-plugin',
        )
        self.assertEqual(
            first=SubPluginGameViewSet.project_model,
            second=SubPlugin,
        )
        self.assertIs(
            expr1=SubPluginGameViewSet.queryset.model,
            expr2=SubPluginGame,
        )
        self.assertDictEqual(
            d1=SubPluginGameViewSet.queryset.query.select_related,
            d2={'game': {}, 'sub_plugin': {}}
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=SubPluginGameViewSet.http_method_names,
            tuple2=('get', 'post', 'delete', 'options'),
        )

    def test_get_list(self):
        # Verify that non logged in user can see results but not 'id'
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        request = response.wsgi_request
        icon = f'{request.scheme}://{request.get_host()}{self.game_2.icon.url}'
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'game': {
                    'name': self.game_2.name,
                    'slug': self.game_2.slug,
                    'icon': icon,
                },
            },
        )

        # Verify that regular user can see results but not 'id'
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'game': {
                    'name': self.game_2.name,
                    'slug': self.game_2.slug,
                    'icon': icon,
                },
            },
        )

        # Verify that contributors can see results AND 'id'
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'game': {
                    'name': self.game_2.name,
                    'slug': self.game_2.slug,
                    'icon': icon,
                },
                'id': str(self.sub_plugin_game_2.id),
            },
        )

        # Verify that the owner can see results AND 'id'
        self.client.force_login(self.owner.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'game': {
                    'name': self.game_2.name,
                    'slug': self.game_2.slug,
                    'icon': icon,
                },
                'id': str(self.sub_plugin_game_2.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.sub_plugin_game_1.id}/'
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot see details
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributors can see details
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=api_path)
        request = response.wsgi_request
        icon = f'{request.scheme}://{request.get_host()}{self.game_1.icon.url}'
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'game': {
                    'name': self.game_1.name,
                    'slug': self.game_1.slug,
                    'icon': icon,
                },
                'id': str(self.sub_plugin_game_1.id),
            },
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
            d2={
                'game': {
                    'name': self.game_1.name,
                    'slug': self.game_1.slug,
                    'icon': icon,
                },
                'id': str(self.sub_plugin_game_1.id),
            },
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
            d2={'detail': 'Invalid sub_plugin_slug.'},
        )

    def test_post(self):
        # Verify that non logged in user cannot add a game
        response = self.client.post(
            path=self.api_path,
            data={'game_slug': self.game_3.slug},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot add a game
        self.client.force_login(self.regular_user.user)
        response = self.client.post(
            path=self.api_path,
            data={'game_slug': self.game_3.slug},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can add a game
        self.client.force_login(self.contributor.user)
        response = self.client.post(
            path=self.api_path,
            data={'game_slug': self.game_3.slug},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

        # Verify that owner can add a game
        self.client.force_login(self.owner.user)
        response = self.client.post(
            path=self.api_path,
            data={'game_slug': self.game_4.slug},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

    def test_post_failure(self):
        self.client.force_login(self.owner.user)

        # Verify existing affiliated game cannot be added
        response = self.client.post(
            path=self.api_path,
            data={'game_slug': self.game_1.slug},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'game': [f'Game already linked to {SubPluginGameViewSet.project_type}.']}
        )

        # Verify non-existing game cannot be added
        invalid_slug = 'invalid'
        response = self.client.post(
            path=self.api_path,
            data={'game_slug': invalid_slug},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'game': [f'Invalid game "{invalid_slug}".']}
        )

    def test_delete(self):
        # Verify that non logged in user cannot delete a game
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_game_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a game
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_game_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a game
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_game_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete a game
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_game_2.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second=f'{self.sub_plugin} - Game',
        )


class SubPluginImageViewSetTestCase(APITestCase):

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
        cls.base_api_path = f'/api/sub-plugins/images/{cls.plugin.slug}/'
        cls.api_path = f'{cls.base_api_path}{cls.sub_plugin.slug}/'
        cls.contributor = ForumUserFactory()
        SubPluginContributorFactory(
            sub_plugin=cls.sub_plugin,
            user=cls.contributor,
        )
        cls.sub_plugin_image_1 = SubPluginImageFactory(
            sub_plugin=cls.sub_plugin,
        )
        cls.sub_plugin_image_2 = SubPluginImageFactory(
            sub_plugin=cls.sub_plugin,
        )
        cls.regular_user = ForumUserFactory()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginImageViewSet, ProjectImageViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginImageViewSet.serializer_class,
            second=SubPluginImageSerializer,
        )
        self.assertEqual(
            first=SubPluginImageViewSet.project_type,
            second='sub-plugin',
        )
        self.assertEqual(
            first=SubPluginImageViewSet.project_model,
            second=SubPlugin,
        )
        self.assertIs(
            expr1=SubPluginImageViewSet.queryset.model,
            expr2=SubPluginImage,
        )
        self.assertDictEqual(
            d1=SubPluginImageViewSet.queryset.query.select_related,
            d2={'sub_plugin': {}},
        )

    def test_parent_project(self):
        obj = SubPluginImageViewSet()
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
        obj = SubPluginImageViewSet()
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
            tuple1=SubPluginImageViewSet.http_method_names,
            tuple2=('get', 'post', 'delete', 'options'),
        )

    def test_get_list(self):
        # Verify that non logged in user can see results but not 'id'
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        request = response.wsgi_request
        image = f'{request.scheme}://{request.get_host()}{self.sub_plugin_image_2.image.url}'
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'image': image,
            },
        )

        # Verify that regular user can see results but not 'id'
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        request = response.wsgi_request
        image = f'{request.scheme}://{request.get_host()}{self.sub_plugin_image_2.image.url}'
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'image': image,
            },
        )

        # Verify that contributors can see results AND 'id'
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'image': image,
                'id': str(self.sub_plugin_image_2.id),
            },
        )

        # Verify that the owner can see results AND 'id'
        self.client.force_login(self.owner.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'image': image,
                'id': str(self.sub_plugin_image_2.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.sub_plugin_image_1.id}/'
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot see details
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributors can see details
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=api_path)
        request = response.wsgi_request
        image = f'{request.scheme}://{request.get_host()}{self.sub_plugin_image_1.image.url}'
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'image': image,
                'id': str(self.sub_plugin_image_1.id),
            },
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
            d2={
                'image': image,
                'id': str(self.sub_plugin_image_1.id),
            },
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
            d2={'detail': 'Invalid sub_plugin_slug.'},
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post(self):
        # Verify that regular user cannot add an image
        self.client.force_login(self.regular_user.user)
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        response = self.client.post(
            path=self.api_path,
            data={'image': tmp_file},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can add an image
        self.client.force_login(self.contributor.user)
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        response = self.client.post(
            path=self.api_path,
            data={'image': tmp_file},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

        # Verify that owner can add an image
        self.client.force_login(self.owner.user)
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        response = self.client.post(
            path=self.api_path,
            data={'image': tmp_file},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

    def test_delete(self):
        # Verify that regular user cannot delete an image
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_image_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete an image
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_image_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete an image
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_image_2.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second=f'{self.sub_plugin} - Image',
        )


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

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second=f'{self.sub_plugin} - Release',
        )


class SubPluginTagViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = plugin = sub_plugin = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory()
        cls.sub_plugin = SubPluginFactory(
            owner=cls.owner,
            plugin=cls.plugin,
        )
        cls.base_api_path = f'/api/sub-plugins/tags/{cls.plugin.slug}/'
        cls.api_path = f'{cls.base_api_path}{cls.sub_plugin.slug}/'
        cls.contributor = ForumUserFactory()
        SubPluginContributorFactory(
            sub_plugin=cls.sub_plugin,
            user=cls.contributor,
        )
        cls.sub_plugin_tag_1 = SubPluginTagFactory(
            sub_plugin=cls.sub_plugin,
        )
        cls.sub_plugin_tag_2 = SubPluginTagFactory(
            sub_plugin=cls.sub_plugin,
        )
        cls.regular_user = ForumUserFactory()

    def test_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginTagViewSet, ProjectTagViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginTagViewSet.serializer_class,
            second=SubPluginTagSerializer,
        )
        self.assertEqual(
            first=SubPluginTagViewSet.project_type,
            second='sub-plugin',
        )
        self.assertEqual(
            first=SubPluginTagViewSet.project_model,
            second=SubPlugin,
        )
        self.assertIs(
            expr1=SubPluginTagViewSet.queryset.model,
            expr2=SubPluginTag,
        )
        self.assertDictEqual(
            d1=SubPluginTagViewSet.queryset.query.select_related,
            d2={'tag': {}, 'sub_plugin': {}}
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=SubPluginTagViewSet.http_method_names,
            tuple2=('get', 'post', 'delete', 'options'),
        )

    def test_get_list(self):
        # Verify that non logged in user can see results but not 'id'
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'tag': self.sub_plugin_tag_2.tag.name,
            },
        )

        # Verify that regular user can see results but not 'id'
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'tag': self.sub_plugin_tag_2.tag.name,
            },
        )

        # Verify that contributors can see results AND 'id'
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'tag': self.sub_plugin_tag_2.tag.name,
                'id': str(self.sub_plugin_tag_2.id),
            },
        )

        # Verify that the owner can see results AND 'id'
        self.client.force_login(self.owner.user)
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'tag': self.sub_plugin_tag_2.tag.name,
                'id': str(self.sub_plugin_tag_2.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.sub_plugin_tag_1.id}/'
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot see details
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
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
            d2={
                'tag': self.sub_plugin_tag_1.tag.name,
                'id': str(self.sub_plugin_tag_1.id),
            },
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
            d2={
                'tag': self.sub_plugin_tag_1.tag.name,
                'id': str(self.sub_plugin_tag_1.id),
            },
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
            d2={'detail': 'Invalid sub_plugin_slug.'},
        )

    def test_post(self):
        # Verify that non logged in user cannot add a tag
        response = self.client.post(
            path=self.api_path,
            data={'tag': 'new-tag-1'},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot add a tag
        self.client.force_login(self.regular_user.user)
        response = self.client.post(
            path=self.api_path,
            data={'tag': 'new-tag-1'},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can add a tag
        self.client.force_login(self.contributor.user)
        response = self.client.post(
            path=self.api_path,
            data={'tag': 'new-tag-1'},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

        # Verify that owner can add a tag
        self.client.force_login(self.owner.user)
        response = self.client.post(
            path=self.api_path,
            data={'tag': 'new-tag-2'},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

    def test_post_failure(self):
        self.client.force_login(self.owner.user)

        # Verify existing affiliated tag cannot be added
        response = self.client.post(
            path=self.api_path,
            data={'tag': self.sub_plugin_tag_1.tag},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'tag': [f'Tag already linked to {SubPluginTagViewSet.project_type}.']}
        )

        # Verify black-listed tag cannot be added
        tag = TagFactory(
            black_listed=True,
        )
        response = self.client.post(
            path=self.api_path,
            data={'tag': tag.name},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'tag': [f"Tag '{tag.name}' is black-listed, unable to add."]}
        )

    def test_delete(self):
        # Verify that non logged in user cannot delete a tag
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_tag_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a tag
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_tag_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a tag
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_tag_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete a tag
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_tag_2.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second=f'{self.sub_plugin} - Tag',
        )


class SubPluginViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = sub_plugin = None
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
        cls.base_api_path = f'/api/sub-plugins/projects/'
        cls.api_path = f'{cls.base_api_path}{plugin.slug}/'
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
        # Verify that non logged in user can see results but not 'id'
        response = self.client.get(path=self.api_path)
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
        SubPluginTagFactory(
            sub_plugin=self.sub_plugin,
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
        SubPluginGameFactory(
            sub_plugin=self.sub_plugin,
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
        api_path = f'{self.api_path}{self.sub_plugin.slug}/'
        response = self.client.get(path=api_path)
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
        # Verify non logged in user cannot create a sub-plugin
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
        api_path = f'{self.base_api_path}{plugin.slug}/'
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

        # Verify that a logged in user can create a sub-plugin
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

    def test_patch(self):
        # Verify that non logged in user cannot update a path
        api_path = f'{self.api_path}{self.sub_plugin.slug}/'
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

        # Verify that regular user cannot update a path
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

        # Verify that contributor can update a path
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

        # Verify that owner can update a path
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
            second='Sub Plugin List',
        )
