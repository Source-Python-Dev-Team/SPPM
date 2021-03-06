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
from rest_framework.parsers import ParseError
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.api.common.views import (
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectTagViewSet,
)
from project_manager.sub_plugins.api.serializers import (
    SubPluginContributorSerializer,
    SubPluginGameSerializer,
    SubPluginImageSerializer,
    SubPluginTagSerializer,
)
from project_manager.sub_plugins.api.views import (
    SubPluginContributorViewSet,
    SubPluginGameViewSet,
    SubPluginImageViewSet,
    SubPluginTagViewSet,
)
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginContributor,
    SubPluginGame,
    SubPluginImage,
    SubPluginTag,
)
from test_utils.factories.games import GameFactory
from test_utils.factories.plugins import PluginFactory
from test_utils.factories.sub_plugins import (
    SubPluginContributorFactory,
    SubPluginFactory,
    SubPluginGameFactory,
    SubPluginImageFactory,
    SubPluginTagFactory,
)
from test_utils.factories.tags import TagFactory
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginContributorViewSetTestCase(APITestCase):

    contributor = detail_api = list_api = owner = plugin = sub_plugin = None
    sub_plugin_contributor = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory()
        cls.sub_plugin = SubPluginFactory(
            plugin=cls.plugin,
            owner=cls.owner,
        )
        cls.contributor = ForumUserFactory()
        cls.sub_plugin_contributor = SubPluginContributorFactory(
            sub_plugin=cls.sub_plugin,
            user=cls.contributor,
        )
        cls.new_contributor = ForumUserFactory()
        cls.regular_user = ForumUserFactory()
        cls.detail_api = 'api:sub-plugins:contributors-detail'
        cls.list_api = 'api:sub-plugins:contributors-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'sub_plugin_slug': cls.sub_plugin.slug,
                'pk': cls.sub_plugin_contributor.id,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'sub_plugin_slug': cls.sub_plugin.slug,
            },
        )

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
                'id': str(self.sub_plugin_contributor.id),
            },
        )

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
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid sub_plugin_slug.'},
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
                    'forum_id': self.sub_plugin_contributor.user.forum_id,
                    'username': self.sub_plugin_contributor.user.user.username,
                },
                'id': str(self.sub_plugin_contributor.id),
            },
        )

    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'sub_plugin_slug': self.sub_plugin.slug,
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
            d2={
                'username': [
                    f'User {self.owner.user.username} is the owner, cannot add as a contributor',
                ],
            },
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
        # Verify that non-logged-in user cannot POST
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot POST
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors cannot POST
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that the owner can POST
        self.client.force_login(user=self.owner.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Contributor',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'POST'})

    def test_options_object(self):
        # Verify that non-logged-in user cannot DELETE
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot DELETE
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors cannot DELETE
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that the owner can DELETE
        self.client.force_login(user=self.owner.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Contributor',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'DELETE'})


class SubPluginGameViewSetTestCase(APITestCase):

    contributor = detail_api = game_1 = game_2 = list_api = owner = None
    plugin = sub_plugin = sub_plugin_game_1 = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory()
        cls.sub_plugin = SubPluginFactory(
            owner=cls.owner,
            plugin=cls.plugin,
        )
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
        cls.detail_api = 'api:sub-plugins:games-detail'
        cls.list_api = 'api:sub-plugins:games-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'sub_plugin_slug': cls.sub_plugin.slug,
                'pk': cls.sub_plugin_game_1.id,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'sub_plugin_slug': cls.sub_plugin.slug,
            },
        )

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
                'id': str(self.sub_plugin_game_2.id),
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
                'id': str(self.sub_plugin_game_2.id),
            },
        )

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
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid sub_plugin_slug.'},
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
                'id': str(self.sub_plugin_game_1.id),
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
                'id': str(self.sub_plugin_game_1.id),
            },
        )

    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'sub_plugin_slug': self.sub_plugin.slug,
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
            d2={'game': [f'Game already linked to {SubPluginGameViewSet.project_type}.']}
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
        response = self.client.delete(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a game
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a game
        self.client.force_login(self.contributor.user)
        response = self.client.delete(path=self.detail_path)
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
                    'sub_plugin_slug': self.sub_plugin.slug,
                    'pk': self.sub_plugin_game_2.id,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        # Verify that non-logged-in user cannot POST
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Game',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot POST
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Game',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can POST
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Game',
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
            second=f'{self.sub_plugin} - Game',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'POST'})

    def test_options_object(self):
        # Verify that non-logged-in user cannot DELETE
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Game',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot DELETE
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Game',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can DELETE
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Game',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'DELETE'})

        # Verify that the owner can DELETE
        self.client.force_login(user=self.owner.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Game',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'DELETE'})


class SubPluginImageViewSetTestCase(APITestCase):

    contributor = detail_api = list_api = owner = plugin = sub_plugin = None
    sub_plugin_image_1 = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory()
        cls.sub_plugin = SubPluginFactory(
            owner=cls.owner,
            plugin=cls.plugin,
        )
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
            created=now() + timedelta(seconds=1)
        )
        cls.regular_user = ForumUserFactory()
        cls.detail_api = 'api:sub-plugins:images-detail'
        cls.list_api = 'api:sub-plugins:images-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'sub_plugin_slug': cls.sub_plugin.slug,
                'pk': cls.sub_plugin_image_1.id,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'sub_plugin_slug': cls.sub_plugin.slug,
            },
        )

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
        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=self.list_path)
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
                'id': str(self.sub_plugin_image_2.id),
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
                'id': str(self.sub_plugin_image_2.id),
            },
        )

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
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid sub_plugin_slug.'},
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
        response = self.client.get(path=self.detail_path)
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

    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'sub_plugin_slug': self.sub_plugin.slug,
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
        # Verify that non-logged-in user cannot add a game
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
        response = self.client.delete(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete an image
        self.client.force_login(self.contributor.user)
        response = self.client.delete(path=self.detail_path)
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
                    'sub_plugin_slug': self.sub_plugin.slug,
                    'pk': self.sub_plugin_image_2.id,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        # Verify that non-logged-in user cannot POST
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Image',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot POST
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Image',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can POST
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Image',
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
            second=f'{self.sub_plugin} - Image',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'POST'})

    def test_options_object(self):
        # Verify that non-logged-in user cannot DELETE
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Image',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot DELETE
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Image',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can DELETE
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Image',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'DELETE'})

        # Verify that the owner can DELETE
        self.client.force_login(user=self.owner.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Image',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'DELETE'})


class SubPluginTagViewSetTestCase(APITestCase):

    contributor = detail_api = list_api = owner = plugin = sub_plugin = None
    sub_plugin_tag_1 = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin = PluginFactory()
        cls.sub_plugin = SubPluginFactory(
            owner=cls.owner,
            plugin=cls.plugin,
        )
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
        cls.detail_api = 'api:sub-plugins:tags-detail'
        cls.list_api = 'api:sub-plugins:tags-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'sub_plugin_slug': cls.sub_plugin.slug,
                'pk': cls.sub_plugin_tag_1.id,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'plugin_slug': cls.plugin.slug,
                'sub_plugin_slug': cls.sub_plugin.slug,
            },
        )

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
                'tag': self.sub_plugin_tag_2.tag.name,
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
                'tag': self.sub_plugin_tag_2.tag.name,
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
                'tag': self.sub_plugin_tag_2.tag.name,
                'id': str(self.sub_plugin_tag_2.id),
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
                'tag': self.sub_plugin_tag_2.tag.name,
                'id': str(self.sub_plugin_tag_2.id),
            },
        )

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
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid sub_plugin_slug.'},
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
                'tag': self.sub_plugin_tag_1.tag.name,
                'id': str(self.sub_plugin_tag_1.id),
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
                'tag': self.sub_plugin_tag_1.tag.name,
                'id': str(self.sub_plugin_tag_1.id),
            },
        )

    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin.slug,
                    'sub_plugin_slug': self.sub_plugin.slug,
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
        response = self.client.delete(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a tag
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(path=self.detail_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a tag
        self.client.force_login(self.contributor.user)
        response = self.client.delete(path=self.detail_path)
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
                    'sub_plugin_slug': self.sub_plugin.slug,
                    'pk': self.sub_plugin_tag_2.id,
                },
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

    def test_options(self):
        # Verify that non-logged-in user cannot POST
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Tag',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot POST
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Tag',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can POST
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Tag',
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
            second=f'{self.sub_plugin} - Tag',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'POST'})

    def test_options_object(self):
        # Verify that non-logged-in user cannot DELETE
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Tag',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot DELETE
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Tag',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can DELETE
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Tag',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'DELETE'})

        # Verify that the owner can DELETE
        self.client.force_login(user=self.owner.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.sub_plugin} - Tag',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'DELETE'})
