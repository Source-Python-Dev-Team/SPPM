# =============================================================================
# IMPORTS
# =============================================================================
# Python
import shutil
import tempfile
from datetime import timedelta

# Django
from django.test import override_settings
from django.utils.timezone import now

# Third Party Python
from path import Path

# Third Party Django
from PIL import Image
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.api.common.views import (
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectTagViewSet,
)
from project_manager.api.common.views.mixins import ProjectThroughModelMixin
from project_manager.plugins.api.serializers import (
    PluginContributorSerializer,
    PluginGameSerializer,
    PluginImageSerializer,
    PluginTagSerializer,
    SubPluginPathSerializer,
)
from project_manager.plugins.api.views import (
    PluginContributorViewSet,
    PluginGameViewSet,
    PluginImageViewSet,
    PluginTagViewSet,
    SubPluginPathViewSet,
)
from project_manager.plugins.models import (
    Plugin,
    PluginContributor,
    PluginGame,
    PluginImage,
    PluginTag,
    SubPluginPath,
)
from test_utils.factories.games import GameFactory
from test_utils.factories.plugins import (
    PluginContributorFactory,
    PluginFactory,
    PluginGameFactory,
    PluginImageFactory,
    PluginTagFactory,
    SubPluginPathFactory,
)
from test_utils.factories.tags import TagFactory
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PluginContributorViewSetTestCase(APITestCase):

    contributor = detail_api = list_api = owner = plugin = None
    plugin_contributor = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
        )
        cls.contributor = ForumUserFactory()
        cls.plugin_contributor = PluginContributorFactory(
            plugin=cls.plugin,
            user=cls.contributor,
        )
        cls.new_contributor = ForumUserFactory()
        cls.regular_user = ForumUserFactory()
        cls.detail_api = 'api:plugins:contributors-detail'
        cls.list_api = 'api:plugins:contributors-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'pk': cls.plugin_contributor.id,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
            },
        )

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
        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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

    def test_get_list_failure(self):
        response = self.client.get(
            path=reverse(
                viewname=self.list_api,
                kwargs={
                    'plugin_slug': 'invalid',
                }
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid plugin_slug.'},
        )

    def test_get_details(self):
        # Verify that non-logged-in user cannot see details
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot see details
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributors cannot see details
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
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
            d2={
                'user': {
                    'forum_id': self.plugin_contributor.user.forum_id,
                    'username': self.plugin_contributor.user.user.username,
                },
                'id': str(self.plugin_contributor.id),
            },
        )

    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'pk': 'invalid',
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Not found.'},
        )

    def test_post(self):
        # Verify that non-logged-in user cannot add a contributor
        response = self.client.post(
            path=self.list_path,
            data={'username': self.new_contributor.user.username},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot add a contributor
        self.client.force_login(self.regular_user.user)
        response = self.client.post(
            path=self.list_path,
            data={'username': self.new_contributor.user.username},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor cannot add a contributor
        self.client.force_login(self.contributor.user)
        response = self.client.post(
            path=self.list_path,
            data={'username': self.new_contributor.user.username},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that owner can add a contributor
        self.client.force_login(self.owner.user)
        response = self.client.post(
            path=self.list_path,
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
            path=self.list_path,
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
            path=self.list_path,
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
            path=self.list_path,
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
        # Verify that non-logged-in user cannot delete a contributor
        response = self.client.delete(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a contributor
        self.client.force_login(self.contributor.user)
        response = self.client.delete(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor cannot delete a contributor
        self.client.force_login(self.contributor.user)
        response = self.client.delete(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that owner can delete a contributor
        self.client.force_login(self.owner.user)
        response = self.client.delete(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second=f'{self.plugin} - Contributor',
        )
        # TODO: test actions

    def test_options_detail(self):
        # TODO: test actions
        pass


class PluginGameViewSetTestCase(APITestCase):

    contributor = detail_api = list_api = owner = game_1 = game_2 = None
    plugin = plugin_game_1 = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
        )
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
        cls.detail_api = 'api:plugins:games-detail'
        cls.list_api = 'api:plugins:games-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'pk': cls.plugin_game_1.id,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
            },
        )

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
        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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

    def test_get_list_failure(self):
        response = self.client.get(
            path=reverse(
                viewname=self.list_api,
                kwargs={
                    'plugin_slug': 'invalid',
                }
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid plugin_slug.'},
        )

    def test_get_details(self):
        # Verify that non-logged-in user cannot see details
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot see details
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributors can see details
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.detail_path)
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
        response = self.client.get(path=self.detail_path)
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

    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'pk': 'invalid',
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Not found.'},
        )

    def test_post(self):
        # Verify that non-logged-in user cannot add a game
        response = self.client.post(
            path=self.list_path,
            data={'game_slug': self.game_3.slug},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot add a game
        self.client.force_login(self.regular_user.user)
        response = self.client.post(
            path=self.list_path,
            data={'game_slug': self.game_3.slug},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can add a game
        self.client.force_login(self.contributor.user)
        response = self.client.post(
            path=self.list_path,
            data={'game_slug': self.game_3.slug},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

        # Verify that owner can add a game
        self.client.force_login(self.owner.user)
        response = self.client.post(
            path=self.list_path,
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
            path=self.list_path,
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
            path=self.list_path,
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
        # Verify that non-logged-in user cannot delete a game
        response = self.client.delete(self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a game
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a game
        self.client.force_login(self.contributor.user)
        response = self.client.delete(self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete a game
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'pk': self.plugin_game_2.id,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second=f'{self.plugin} - Game',
        )
        # TODO: test actions

    def test_options_detail(self):
        # TODO: test actions
        pass


class PluginImageViewSetTestCase(APITestCase):

    contributor = detail_api = list_api = owner = plugin = None
    plugin_image_1 = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
        )
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
            created=now() + timedelta(seconds=1)
        )
        cls.regular_user = ForumUserFactory()
        cls.detail_api = 'api:plugins:images-detail'
        cls.list_api = 'api:plugins:images-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'pk': cls.plugin_image_1.id,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
            },
        )

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
        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        request = response.wsgi_request
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'image': image,
            },
        )

        # Verify that contributors can see results AND 'id'
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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

    def test_get_list_failure(self):
        response = self.client.get(
            path=reverse(
                viewname=self.list_api,
                kwargs={
                    'plugin_slug': 'invalid',
                }
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid plugin_slug.'},
        )

    def test_get_details(self):
        # Verify that non-logged-in user cannot see details
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot see details
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributors can see details
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.detail_path)
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
        response = self.client.get(path=self.detail_path)
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

    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'pk': 'invalid',
                },
            ),
        )
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
        # Verify that regular user cannot add an image
        self.client.force_login(self.regular_user.user)
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        response = self.client.post(
            path=self.list_path,
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
            path=self.list_path,
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
            path=self.list_path,
            data={'image': tmp_file},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

    def test_delete(self):
        # Verify that non-logged-in user cannot delete a game
        response = self.client.delete(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete an image
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete an image
        self.client.force_login(self.contributor.user)
        response = self.client.delete(self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete an image
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'pk': self.plugin_image_2.id,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second=f'{self.plugin} - Image',
        )
        # TODO: test actions

    def test_options_detail(self):
        # TODO: test actions
        pass


class PluginTagViewSetTestCase(APITestCase):

    contributor = detail_api = list_api = owner = plugin = plugin_tag_1 = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
        )
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
        cls.detail_api = 'api:plugins:tags-detail'
        cls.list_api = 'api:plugins:tags-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'pk': cls.plugin_tag_1.id,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
            },
        )

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
        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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

    def test_get_list_failure(self):
        response = self.client.get(
            path=reverse(
                viewname=self.list_api,
                kwargs={
                    'plugin_slug': 'invalid',
                }
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid plugin_slug.'},
        )

    def test_get_details(self):
        # Verify that non-logged-in user cannot see details
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot see details
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
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
            d2={
                'tag': self.plugin_tag_1.tag.name,
                'id': str(self.plugin_tag_1.id),
            },
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
            d2={
                'tag': self.plugin_tag_1.tag.name,
                'id': str(self.plugin_tag_1.id),
            },
        )

    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'pk': 'invalid',
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Not found.'},
        )

    def test_post(self):
        # Verify that non-logged-in user cannot add a tag
        response = self.client.post(
            path=self.list_path,
            data={'tag': 'new-tag-1'},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot add a tag
        self.client.force_login(self.regular_user.user)
        response = self.client.post(
            path=self.list_path,
            data={'tag': 'new-tag-1'},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can add a tag
        self.client.force_login(self.contributor.user)
        response = self.client.post(
            path=self.list_path,
            data={'tag': 'new-tag-1'},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_201_CREATED,
        )

        # Verify that owner can add a tag
        self.client.force_login(self.owner.user)
        response = self.client.post(
            path=self.list_path,
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
            path=self.list_path,
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
            path=self.list_path,
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
        # Verify that non-logged-in user cannot delete a tag
        response = self.client.delete(self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a tag
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a tag
        self.client.force_login(self.contributor.user)
        response = self.client.delete(self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete a tag
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'pk': self.plugin_tag_2.id,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second=f'{self.plugin} - Tag',
        )
        # TODO: test actions

    def test_options_detail(self):
        # TODO: test actions
        pass


class SubPluginPathViewSetTestCase(APITestCase):

    contributor = detail_api = list_api = owner = plugin = None
    sub_plugin_path_1 = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory(
            owner=cls.owner,
        )
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
        cls.detail_api = 'api:plugins:paths-detail'
        cls.list_api = 'api:plugins:paths-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'pk': cls.sub_plugin_path_1.id,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
            },
        )

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
        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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
        response = self.client.get(path=self.list_path)
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

    def test_get_list_failure(self):
        response = self.client.get(
            path=reverse(
                viewname=self.list_api,
                kwargs={
                    'plugin_slug': 'invalid',
                }
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid plugin_slug.'},
        )

    def test_get_details(self):
        # Verify that non-logged-in user cannot see details
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot see details
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
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
        response = self.client.get(path=self.detail_path)
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

    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'pk': 'invalid',
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Not found.'},
        )

    def test_post(self):
        # Verify that non-logged-in user cannot add a path
        response = self.client.post(
            path=self.list_path,
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
            path=self.list_path,
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
            path=self.list_path,
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
            path=self.list_path,
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
        # Verify that non-logged-in user cannot update a path
        response = self.client.patch(
            path=self.detail_path,
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
            path=self.detail_path,
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
            path=self.detail_path,
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
            path=self.detail_path,
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
        # Verify that non-logged-in user cannot delete a path
        response = self.client.delete(self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a path
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a path
        self.client.force_login(self.contributor.user)
        response = self.client.delete(self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete a path
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'pk': self.sub_plugin_path_2.id,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['name'],
            second=f'{self.plugin} - Sub-Plugin Path',
        )
        # TODO: test actions

    def test_options_detail(self):
        # TODO: test actions
        pass
