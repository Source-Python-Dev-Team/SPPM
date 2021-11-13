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
from project_manager.common.api.views.mixins import ProjectThroughModelMixin
from project_manager.plugins.api.filtersets import PluginFilterSet
from project_manager.plugins.api.serializers import (
    PluginContributorSerializer,
    PluginCreateSerializer,
    PluginGameSerializer,
    PluginImageSerializer,
    PluginReleaseSerializer,
    PluginSerializer,
    PluginTagSerializer,
    SubPluginPathSerializer,
)
from project_manager.plugins.api.views import (
    PluginAPIView,
    PluginContributorViewSet,
    PluginGameViewSet,
    PluginImageViewSet,
    PluginReleaseViewSet,
    PluginTagViewSet,
    PluginViewSet,
    SubPluginPathViewSet,
)
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
from requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from test_utils.factories.games import GameFactory
from test_utils.factories.packages import PackageFactory, PackageReleaseFactory
from test_utils.factories.plugins import (
    PluginContributorFactory,
    PluginFactory,
    PluginGameFactory,
    PluginImageFactory,
    PluginReleaseFactory,
    PluginTagFactory,
    SubPluginPathFactory,
)
from test_utils.factories.tags import TagFactory
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PluginAPIViewTestCase(APITestCase):

    api_path = '/api/plugins/'

    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PluginAPIView, ProjectAPIView))

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginAPIView.project_type,
            second='plugin',
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PluginAPIView.http_method_names,
            tuple2=('get', 'options'),
        )

    def test_get(self):
        response = self.client.get(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        base_path = reverse(
            viewname=f'api:plugins:endpoints',
            request=response.wsgi_request,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'contributors': base_path + f'contributors/<plugin>/',
                'games': base_path + f'games/<plugin>/',
                'images': base_path + f'images/<plugin>/',
                'projects': base_path + f'projects/',
                'releases': base_path + f'releases/<plugin>/',
                'tags': base_path + f'tags/<plugin>/',
                'paths': base_path + f'paths/<plugin>/',
            }
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(first=response.json()['name'], second='Plugin APIs')


class PluginContributorViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = plugin = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/plugins/contributors/'
        cls.api_path = f'{cls.base_api_path}{cls.plugin.slug}/'
        cls.contributor = ForumUserFactory()
        cls.plugin_contributor = PluginContributorFactory(
            plugin=cls.plugin,
            user=cls.contributor,
        )
        cls.new_contributor = ForumUserFactory()
        cls.regular_user = ForumUserFactory()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PluginContributorViewSet,
                ProjectContributorViewSet,
            ),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginContributorViewSet.serializer_class,
            second=PluginContributorSerializer,
        )
        self.assertEqual(
            first=PluginContributorViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=PluginContributorViewSet.project_model,
            second=Plugin,
        )
        self.assertIs(
            expr1=PluginContributorViewSet.queryset.model,
            expr2=PluginContributor,
        )
        self.assertDictEqual(
            d1=PluginContributorViewSet.queryset.query.select_related,
            d2={'user': {'user': {}}, 'plugin': {}}
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PluginContributorViewSet.http_method_names,
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
                'id': str(self.plugin_contributor.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.plugin_contributor.id}/'
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
                    'forum_id': self.plugin_contributor.user.forum_id,
                    'username': self.plugin_contributor.user.user.username,
                },
                'id': str(self.plugin_contributor.id),
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
            d2={'detail': 'Invalid plugin_slug.'},
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
            path=self.api_path + f'{self.plugin_contributor.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a contributor
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.plugin_contributor.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor cannot delete a contributor
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.plugin_contributor.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that owner can delete a contributor
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.plugin_contributor.id}/',
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
            second=f'{self.plugin} - Contributor',
        )


class PluginGameViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = game_1 = game_2 = plugin = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/plugins/games/'
        cls.api_path = f'{cls.base_api_path}{cls.plugin.slug}/'
        cls.contributor = ForumUserFactory()
        PluginContributorFactory(
            plugin=cls.plugin,
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
        cls.plugin_game_1 = PluginGameFactory(
            plugin=cls.plugin,
            game=cls.game_1,
        )
        cls.plugin_game_2 = PluginGameFactory(
            plugin=cls.plugin,
            game=cls.game_2,
        )
        cls.regular_user = ForumUserFactory()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginGameViewSet, ProjectGameViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginGameViewSet.serializer_class,
            second=PluginGameSerializer,
        )
        self.assertEqual(
            first=PluginGameViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=PluginGameViewSet.project_model,
            second=Plugin,
        )
        self.assertIs(
            expr1=PluginGameViewSet.queryset.model,
            expr2=PluginGame,
        )
        self.assertDictEqual(
            d1=PluginGameViewSet.queryset.query.select_related,
            d2={'game': {}, 'plugin': {}}
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PluginGameViewSet.http_method_names,
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
                'id': str(self.plugin_game_2.id),
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
                'id': str(self.plugin_game_2.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.plugin_game_1.id}/'
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
                'id': str(self.plugin_game_1.id),
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
                'id': str(self.plugin_game_1.id),
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
            d2={'detail': 'Invalid plugin_slug.'},
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
            d2={'game': [f'Game already linked to {PluginGameViewSet.project_type}.']}
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
            path=self.api_path + f'{self.plugin_game_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a game
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(
            path=self.api_path + f'{self.plugin_game_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a game
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.plugin_game_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete a game
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.plugin_game_2.id}/',
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
            second=f'{self.plugin} - Game',
        )


class PluginImageViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = plugin = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/plugins/images/'
        cls.api_path = f'{cls.base_api_path}{cls.plugin.slug}/'
        cls.contributor = ForumUserFactory()
        PluginContributorFactory(
            plugin=cls.plugin,
            user=cls.contributor,
        )
        cls.plugin_image_1 = PluginImageFactory(
            plugin=cls.plugin,
        )
        cls.plugin_image_2 = PluginImageFactory(
            plugin=cls.plugin,
        )
        cls.regular_user = ForumUserFactory()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginImageViewSet, ProjectImageViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginImageViewSet.serializer_class,
            second=PluginImageSerializer,
        )
        self.assertEqual(
            first=PluginImageViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=PluginImageViewSet.project_model,
            second=Plugin,
        )
        self.assertIs(
            expr1=PluginImageViewSet.queryset.model,
            expr2=PluginImage,
        )
        self.assertDictEqual(
            d1=PluginImageViewSet.queryset.query.select_related,
            d2={'plugin': {}},
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PluginImageViewSet.http_method_names,
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
        image = f'{request.scheme}://{request.get_host()}{self.plugin_image_2.image.url}'
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
        image = f'{request.scheme}://{request.get_host()}{self.plugin_image_2.image.url}'
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
                'id': str(self.plugin_image_2.id),
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
                'id': str(self.plugin_image_2.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.plugin_image_1.id}/'
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
        image = f'{request.scheme}://{request.get_host()}{self.plugin_image_1.image.url}'
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'image': image,
                'id': str(self.plugin_image_1.id),
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
                'id': str(self.plugin_image_1.id),
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
            d2={'detail': 'Invalid plugin_slug.'},
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
            path=self.api_path + f'{self.plugin_image_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete an image
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.plugin_image_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete an image
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.plugin_image_2.id}/',
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
            second=f'{self.plugin} - Image',
        )


class PluginReleaseViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = plugin = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/plugins/releases/'
        cls.api_path = f'{cls.base_api_path}{cls.plugin.slug}/'
        cls.contributor = ForumUserFactory()
        PluginContributorFactory(
            plugin=cls.plugin,
            user=cls.contributor,
        )
        cls.plugin_release = PluginReleaseFactory(
            plugin=cls.plugin,
            zip_file='release_v1.0.0.zip',
        )
        cls.regular_user = ForumUserFactory()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PluginReleaseViewSet, ProjectReleaseViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginReleaseViewSet.serializer_class,
            second=PluginReleaseSerializer,
        )
        self.assertEqual(
            first=PluginReleaseViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=PluginReleaseViewSet.project_model,
            second=Plugin,
        )
        self.assertIs(
            expr1=PluginReleaseViewSet.queryset.model,
            expr2=PluginRelease,
        )
        self.assertDictEqual(
            d1=PluginReleaseViewSet.queryset.query.select_related,
            d2={'plugin': {}},
        )
        prefetch_lookups = PluginReleaseViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=4)

        lookup = prefetch_lookups[0]
        self.assertEqual(
            first=lookup.prefetch_to,
            second='pluginreleasepackagerequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PluginReleasePackageRequirement,
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
            second='pluginreleasedownloadrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PluginReleaseDownloadRequirement,
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
            second='pluginreleasepypirequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PluginReleasePyPiRequirement,
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
            second='pluginreleaseversioncontrolrequirement_set',
        )
        self.assertIs(
            expr1=lookup.queryset.model,
            expr2=PluginReleaseVersionControlRequirement,
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
            tuple1=PluginReleaseViewSet.http_method_names,
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
        timestamp = self.plugin_release.created
        request = response.wsgi_request
        zip_file = f'{request.scheme}://{request.get_host()}{self.plugin_release.zip_file.url}'
        payload = {
            'notes': self.plugin_release.notes,
            'zip_file': zip_file,
            'version': self.plugin_release.version,
            'created': {
                'actual': timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'locale': formats.date_format(timestamp, 'DATETIME_FORMAT'),
                'locale_short': formats.date_format(timestamp, 'SHORT_DATETIME_FORMAT'),
            },
            'download_count': self.plugin_release.download_count,
            'download_requirements': [],
            'package_requirements': [],
            'pypi_requirements': [],
            'vcs_requirements': [],
            'id': str(self.plugin_release.id),
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
        api_path = f'{self.api_path}{self.plugin_release.version}/'
        response = self.client.get(path=api_path)
        timestamp = self.plugin_release.created
        request = response.wsgi_request
        zip_file = f'{request.scheme}://{request.get_host()}{self.plugin_release.zip_file.url}'
        payload = {
            'notes': self.plugin_release.notes,
            'zip_file': zip_file,
            'version': self.plugin_release.version,
            'created': {
                'actual': timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'locale': formats.date_format(timestamp, 'DATETIME_FORMAT'),
                'locale_short': formats.date_format(timestamp, 'SHORT_DATETIME_FORMAT'),
            },
            'download_count': self.plugin_release.download_count,
            'download_requirements': [],
            'package_requirements': [],
            'pypi_requirements': [],
            'vcs_requirements': [],
            'id': str(self.plugin_release.id),
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
            d2={'detail': 'Invalid plugin_slug.'},
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post(self):
        plugin = PluginFactory(
            basename='test_plugin',
            owner=self.owner,
        )
        PluginReleaseFactory(
            plugin=plugin,
            version='1.0.0',
        )
        PluginContributorFactory(
            plugin=plugin,
            user=self.contributor,
        )
        api_path = f'{self.base_api_path}{plugin.slug}/'
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'plugins'
        file_path = base_path / 'test-plugin' / 'test-plugin-v1.0.0.zip'

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
            first=plugin.releases.count(),
            second=2,
        )
        content = response.json()
        release = plugin.releases.get(pk=content['id'])
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
            first=plugin.releases.count(),
            second=3,
        )
        content = response.json()
        release = plugin.releases.get(pk=content['id'])
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
        zip_basename = plugin.basename
        plugin = PluginFactory(
            owner=self.owner,
        )
        PluginReleaseFactory(
            plugin=plugin,
            version='1.0.0',
        )
        api_path = f'{self.base_api_path}{plugin.slug}/'
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
                    f" for plugin '{plugin.basename}'.",
                ],
            }
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post_with_requirements(self):
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'plugins'
        file_path = base_path / 'test-plugin' / 'test-plugin-requirements-v1.0.0.zip'
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
        plugin = PluginFactory(
            basename='test_plugin',
            owner=self.owner,
        )
        PluginReleaseFactory(
            plugin=plugin,
            version='1.0.0',
        )
        api_path = f'{self.base_api_path}{plugin.slug}/'
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
        release = PluginRelease.objects.get(pk=response.json()['id'])
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
            second=f'{self.plugin} - Release',
        )


class PluginTagViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = plugin = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/plugins/tags/'
        cls.api_path = f'{cls.base_api_path}{cls.plugin.slug}/'
        cls.contributor = ForumUserFactory()
        PluginContributorFactory(
            plugin=cls.plugin,
            user=cls.contributor,
        )
        cls.plugin_tag_1 = PluginTagFactory(
            plugin=cls.plugin,
        )
        cls.plugin_tag_2 = PluginTagFactory(
            plugin=cls.plugin,
        )
        cls.regular_user = ForumUserFactory()

    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PluginTagViewSet, ProjectTagViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginTagViewSet.serializer_class,
            second=PluginTagSerializer,
        )
        self.assertEqual(
            first=PluginTagViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=PluginTagViewSet.project_model,
            second=Plugin,
        )
        self.assertIs(
            expr1=PluginTagViewSet.queryset.model,
            expr2=PluginTag,
        )
        self.assertDictEqual(
            d1=PluginTagViewSet.queryset.query.select_related,
            d2={'tag': {}, 'plugin': {}}
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PluginTagViewSet.http_method_names,
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
                'tag': self.plugin_tag_2.tag.name,
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
                'tag': self.plugin_tag_2.tag.name,
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
                'tag': self.plugin_tag_2.tag.name,
                'id': str(self.plugin_tag_2.id),
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
                'tag': self.plugin_tag_2.tag.name,
                'id': str(self.plugin_tag_2.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.plugin_tag_1.id}/'
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
                'tag': self.plugin_tag_1.tag.name,
                'id': str(self.plugin_tag_1.id),
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
                'tag': self.plugin_tag_1.tag.name,
                'id': str(self.plugin_tag_1.id),
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
            d2={'detail': 'Invalid plugin_slug.'},
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
            data={'tag': self.plugin_tag_1.tag},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'tag': [f'Tag already linked to {PluginTagViewSet.project_type}.']}
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
            path=self.api_path + f'{self.plugin_tag_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a tag
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(
            path=self.api_path + f'{self.plugin_tag_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a tag
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.plugin_tag_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete a tag
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.plugin_tag_2.id}/',
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
            second=f'{self.plugin} - Tag',
        )


class PluginViewSetTestCase(APITestCase):

    contributor = owner = plugin = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
            logo='logo.jpg',
        )
        cls.plugin_release = PluginReleaseFactory(
            plugin=cls.plugin,
            zip_file='/media/release_v1.0.0.zip',
        )
        cls.api_path = f'/api/plugins/projects/'
        cls.contributor = ForumUserFactory()
        PluginContributorFactory(
            plugin=cls.plugin,
            user=cls.contributor,
        )
        cls.regular_user = ForumUserFactory()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PluginViewSet, ProjectViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginViewSet.filterset_class,
            second=PluginFilterSet,
        )
        self.assertEqual(
            first=PluginViewSet.serializer_class,
            second=PluginSerializer,
        )
        self.assertEqual(
            first=PluginViewSet.creation_serializer_class,
            second=PluginCreateSerializer,
        )
        self.assertIs(expr1=PluginViewSet.queryset.model, expr2=Plugin)
        prefetch_lookups = PluginViewSet.queryset._prefetch_related_lookups
        self.assertEqual(first=len(prefetch_lookups), second=1)
        lookup = prefetch_lookups[0]
        self.assertEqual(first=lookup.prefetch_to, second='releases')
        self.assertEqual(
            first=lookup.queryset.query.order_by,
            second=('-created',),
        )
        self.assertDictEqual(
            d1=PluginViewSet.queryset.query.select_related,
            d2={'owner': {'user': {}}},
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PluginViewSet.http_method_names,
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
        zip_file = f'{domain}{self.plugin_release.get_absolute_url()}'
        logo = f'{domain}{self.plugin.logo.url}'
        self.assertEqual(first=content['count'], second=1)
        created_timestamp = self.plugin.created
        updated_timestamp = self.plugin.updated
        payload = {
            'name': self.plugin.name,
            'slug': self.plugin.slug,
            'total_downloads': self.plugin.total_downloads,
            'current_release': {
                'version': self.plugin_release.version,
                'notes': self.plugin_release.notes,
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
            'synopsis': self.plugin.synopsis,
            'description': self.plugin.description,
            'configuration': self.plugin.configuration,
            'logo': logo,
            'video': self.plugin.video,
            'owner': {
                'forum_id': self.plugin.owner.forum_id,
                'username': self.plugin.owner.user.username,
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
        PluginTagFactory(
            plugin=self.plugin,
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
        PluginGameFactory(
            plugin=self.plugin,
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
        api_path = f'{self.api_path}{self.plugin.slug}/'
        response = self.client.get(path=api_path)
        request = response.wsgi_request
        domain = f'{request.scheme}://{request.get_host()}'
        zip_file = f'{domain}{self.plugin_release.get_absolute_url()}'
        logo = f'{domain}{self.plugin.logo.url}'
        created_timestamp = self.plugin.created
        updated_timestamp = self.plugin.updated
        payload = {
            'name': self.plugin.name,
            'slug': self.plugin.slug,
            'total_downloads': self.plugin.total_downloads,
            'current_release': {
                'version': self.plugin_release.version,
                'notes': self.plugin_release.notes,
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
            'synopsis': self.plugin.synopsis,
            'description': self.plugin.description,
            'configuration': self.plugin.configuration,
            'logo': logo,
            'video': self.plugin.video,
            'owner': {
                'forum_id': self.plugin.owner.forum_id,
                'username': self.plugin.owner.user.username,
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
        # Verify non logged in user cannot create a plugin
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'plugins'
        file_path = base_path / 'test-plugin' / 'test-plugin-v1.0.0.zip'
        version = '1.0.0'
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=self.api_path,
                data={
                    'name': 'Test Plugin',
                    'releases.notes': '',
                    'releases.version': version,
                    'releases.zip_file': zip_file,
                },
            )

        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that a logged in user can create a plugin
        self.assertEqual(
            first=Plugin.objects.count(),
            second=1,
        )
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            self.client.force_login(self.regular_user.user)
            response = self.client.post(
                path=self.api_path,
                data={
                    'name': 'Test Plugin',
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
            first=Plugin.objects.count(),
            second=2,
        )
        content = response.json()
        plugin = Plugin.objects.get(slug=content['slug'])
        self.assertEqual(
            first=plugin.releases.count(),
            second=1,
        )
        release = plugin.releases.get()
        self.assertEqual(
            first=release.version,
            second=version,
        )

        # Verify cannot create a plugin where the basename already exists
        with file_path.open('rb') as open_file:
            zip_file = UploadedFile(open_file, content_type='application/zip')
            response = self.client.post(
                path=self.api_path,
                data={
                    'name': 'Test Plugin',
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
            d2={'basename': 'Plugin already exists. Cannot create.'}
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_post_with_requirements(self):
        base_path = settings.BASE_DIR / 'fixtures' / 'releases' / 'plugins'
        file_path = base_path / 'test-plugin' / 'test-plugin-requirements-v1.0.0.zip'
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
                    'name': 'Test Plugin',
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
        plugin = Plugin.objects.get(slug=contents['slug'])
        release = PluginRelease.objects.get(plugin=plugin)
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
        # Verify that non logged in user cannot update a path
        api_path = f'{self.api_path}{self.plugin.slug}/'
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
            second='Plugin List',
        )


class SubPluginPathViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = plugin = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/plugins/paths/'
        cls.api_path = f'{cls.base_api_path}{cls.plugin.slug}/'
        cls.contributor = ForumUserFactory()
        PluginContributorFactory(
            plugin=cls.plugin,
            user=cls.contributor,
        )
        cls.sub_plugin_path_1 = SubPluginPathFactory(
            plugin=cls.plugin,
            allow_module=True,
        )
        cls.sub_plugin_path_2 = SubPluginPathFactory(
            plugin=cls.plugin,
            allow_package_using_basename=True,
        )
        cls.regular_user = ForumUserFactory()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(SubPluginPathViewSet, ProjectThroughModelMixin),
        )

    def test_base_attributes(self):
        self.assertTupleEqual(
            tuple1=SubPluginPathViewSet.ordering,
            tuple2=('path',),
        )
        self.assertEqual(
            first=SubPluginPathViewSet.serializer_class,
            second=SubPluginPathSerializer,
        )
        self.assertEqual(
            first=SubPluginPathViewSet.project_type,
            second='plugin',
        )
        self.assertEqual(
            first=SubPluginPathViewSet.project_model,
            second=Plugin,
        )
        self.assertEqual(
            first=SubPluginPathViewSet.related_model_type,
            second='Sub-Plugin Path',
        )
        self.assertIs(
            expr1=SubPluginPathViewSet.queryset.model,
            expr2=SubPluginPath,
        )
        self.assertDictEqual(
            d1=SubPluginPathViewSet.queryset.query.select_related,
            d2={'plugin': {}},
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=SubPluginPathViewSet.http_method_names,
            tuple2=('get', 'post', 'patch', 'delete', 'options'),
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
                'path': self.sub_plugin_path_1.path,
                'allow_module': self.sub_plugin_path_1.allow_module,
                'allow_package_using_init': self.sub_plugin_path_1.allow_package_using_init,
                'allow_package_using_basename': self.sub_plugin_path_1.allow_package_using_basename,
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
                'path': self.sub_plugin_path_1.path,
                'allow_module': self.sub_plugin_path_1.allow_module,
                'allow_package_using_init': self.sub_plugin_path_1.allow_package_using_init,
                'allow_package_using_basename': self.sub_plugin_path_1.allow_package_using_basename,
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
                'path': self.sub_plugin_path_1.path,
                'allow_module': self.sub_plugin_path_1.allow_module,
                'allow_package_using_init': self.sub_plugin_path_1.allow_package_using_init,
                'allow_package_using_basename': self.sub_plugin_path_1.allow_package_using_basename,
                'id': str(self.sub_plugin_path_1.id),
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
                'path': self.sub_plugin_path_1.path,
                'allow_module': self.sub_plugin_path_1.allow_module,
                'allow_package_using_init': self.sub_plugin_path_1.allow_package_using_init,
                'allow_package_using_basename': self.sub_plugin_path_1.allow_package_using_basename,
                'id': str(self.sub_plugin_path_1.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.sub_plugin_path_1.id}/'
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
                'path': self.sub_plugin_path_1.path,
                'allow_module': self.sub_plugin_path_1.allow_module,
                'allow_package_using_init': self.sub_plugin_path_1.allow_package_using_init,
                'allow_package_using_basename': self.sub_plugin_path_1.allow_package_using_basename,
                'id': str(self.sub_plugin_path_1.id),
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
                'path': self.sub_plugin_path_1.path,
                'allow_module': self.sub_plugin_path_1.allow_module,
                'allow_package_using_init': self.sub_plugin_path_1.allow_package_using_init,
                'allow_package_using_basename': self.sub_plugin_path_1.allow_package_using_basename,
                'id': str(self.sub_plugin_path_1.id),
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
            d2={'detail': 'Invalid plugin_slug.'},
        )

    def test_post(self):
        # Verify that non logged in user cannot add a path
        response = self.client.post(
            path=self.api_path,
            data={
                'path': 'new-path-1',
                'allow_module': False,
                'allow_package_using_init': True,
                'allow_package_using_basename': False,
            },
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot add a path
        self.client.force_login(self.regular_user.user)
        response = self.client.post(
            path=self.api_path,
            data={
                'path': 'new-path-1',
                'allow_module': False,
                'allow_package_using_init': True,
                'allow_package_using_basename': False,
            },
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can add a path
        self.client.force_login(self.contributor.user)
        response = self.client.post(
            path=self.api_path,
            data={
                'path': 'new-path-1',
                'allow_module': False,
                'allow_package_using_init': True,
                'allow_package_using_basename': False,
            },
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

        # Verify that owner can add a path
        self.client.force_login(self.owner.user)
        response = self.client.post(
            path=self.api_path,
            data={
                'path': 'new-path-2',
                'allow_module': False,
                'allow_package_using_init': True,
                'allow_package_using_basename': True,
            },
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

    def test_patch(self):
        # Verify that non logged in user cannot update a path
        api_path = f'{self.api_path}{self.sub_plugin_path_1.id}/'
        response = self.client.patch(
            path=api_path,
            data={
                'allow_module': False,
                'allow_package_using_init': True,
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
                'allow_module': False,
                'allow_package_using_init': True,
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
                'allow_module': False,
                'allow_package_using_init': True,
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
                'allow_module': True,
                'allow_package_using_init': False,
            }
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )

    def test_delete(self):
        # Verify that non logged in user cannot delete a path
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_path_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a path
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_path_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a path
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_path_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete a path
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.sub_plugin_path_2.id}/',
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
            second=f'{self.plugin} - Sub-Plugin Path',
        )
