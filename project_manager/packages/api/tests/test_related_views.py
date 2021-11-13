# =============================================================================
# IMPORTS
# =============================================================================
# Python
import shutil
import tempfile

# Django
from django.test import override_settings

# Third Party Python
from path import Path

# Third Party Django
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

# App
from project_manager.common.api.views import (
    ProjectContributorViewSet,
    ProjectGameViewSet,
    ProjectImageViewSet,
    ProjectTagViewSet,
)
from project_manager.packages.api.serializers import (
    PackageContributorSerializer,
    PackageGameSerializer,
    PackageImageSerializer,
    PackageTagSerializer,
)
from project_manager.packages.api.views import (
    PackageContributorViewSet,
    PackageGameViewSet,
    PackageImageViewSet,
    PackageTagViewSet,
)
from project_manager.packages.models import (
    Package,
    PackageContributor,
    PackageGame,
    PackageImage,
    PackageTag,
)
from test_utils.factories.games import GameFactory
from test_utils.factories.packages import (
    PackageFactory,
    PackageContributorFactory,
    PackageGameFactory,
    PackageImageFactory,
    PackageTagFactory,
)
from test_utils.factories.tags import TagFactory
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PackageContributorViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = package = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.package = PackageFactory(
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/packages/contributors/'
        cls.api_path = f'{cls.base_api_path}{cls.package.slug}/'
        cls.contributor = ForumUserFactory()
        cls.package_contributor = PackageContributorFactory(
            package=cls.package,
            user=cls.contributor,
        )
        cls.new_contributor = ForumUserFactory()
        cls.regular_user = ForumUserFactory()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(
                PackageContributorViewSet,
                ProjectContributorViewSet,
            ),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageContributorViewSet.serializer_class,
            second=PackageContributorSerializer,
        )
        self.assertEqual(
            first=PackageContributorViewSet.project_type,
            second='package',
        )
        self.assertEqual(
            first=PackageContributorViewSet.project_model,
            second=Package,
        )
        self.assertIs(
            expr1=PackageContributorViewSet.queryset.model,
            expr2=PackageContributor,
        )
        self.assertDictEqual(
            d1=PackageContributorViewSet.queryset.query.select_related,
            d2={'user': {'user': {}}, 'package': {}}
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PackageContributorViewSet.http_method_names,
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
                'id': str(self.package_contributor.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.package_contributor.id}/'
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
                    'forum_id': self.package_contributor.user.forum_id,
                    'username': self.package_contributor.user.user.username,
                },
                'id': str(self.package_contributor.id),
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
            d2={'detail': 'Invalid package_slug.'},
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
            path=self.api_path + f'{self.package_contributor.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a contributor
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.package_contributor.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor cannot delete a contributor
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.package_contributor.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that owner can delete a contributor
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.package_contributor.id}/',
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
            second=f'{self.package} - Contributor',
        )


class PackageGameViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = game_1 = game_2 = package = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.package = PackageFactory(
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/packages/games/'
        cls.api_path = f'{cls.base_api_path}{cls.package.slug}/'
        cls.contributor = ForumUserFactory()
        PackageContributorFactory(
            package=cls.package,
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
        cls.package_game_1 = PackageGameFactory(
            package=cls.package,
            game=cls.game_1,
        )
        cls.package_game_2 = PackageGameFactory(
            package=cls.package,
            game=cls.game_2,
        )
        cls.regular_user = ForumUserFactory()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageGameViewSet, ProjectGameViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageGameViewSet.serializer_class,
            second=PackageGameSerializer,
        )
        self.assertEqual(
            first=PackageGameViewSet.project_type,
            second='package',
        )
        self.assertEqual(
            first=PackageGameViewSet.project_model,
            second=Package,
        )
        self.assertIs(
            expr1=PackageGameViewSet.queryset.model,
            expr2=PackageGame,
        )
        self.assertDictEqual(
            d1=PackageGameViewSet.queryset.query.select_related,
            d2={'game': {}, 'package': {}}
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PackageGameViewSet.http_method_names,
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
                'id': str(self.package_game_2.id),
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
                'id': str(self.package_game_2.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.package_game_1.id}/'
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
                'id': str(self.package_game_1.id),
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
                'id': str(self.package_game_1.id),
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
            d2={'detail': 'Invalid package_slug.'},
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
            d2={'game': [f'Game already linked to {PackageGameViewSet.project_type}.']}
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
            path=self.api_path + f'{self.package_game_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a game
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(
            path=self.api_path + f'{self.package_game_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a game
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.package_game_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete a game
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.package_game_2.id}/',
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
            second=f'{self.package} - Game',
        )


class PackageImageViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = package = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.package = PackageFactory(
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/packages/images/'
        cls.api_path = f'{cls.base_api_path}{cls.package.slug}/'
        cls.contributor = ForumUserFactory()
        PackageContributorFactory(
            package=cls.package,
            user=cls.contributor,
        )
        cls.package_image_1 = PackageImageFactory(
            package=cls.package,
        )
        cls.package_image_2 = PackageImageFactory(
            package=cls.package,
        )
        cls.regular_user = ForumUserFactory()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_inheritance(self):
        self.assertTrue(
            expr=issubclass(PackageImageViewSet, ProjectImageViewSet),
        )

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageImageViewSet.serializer_class,
            second=PackageImageSerializer,
        )
        self.assertEqual(
            first=PackageImageViewSet.project_type,
            second='package',
        )
        self.assertEqual(
            first=PackageImageViewSet.project_model,
            second=Package,
        )
        self.assertIs(
            expr1=PackageImageViewSet.queryset.model,
            expr2=PackageImage,
        )
        self.assertDictEqual(
            d1=PackageImageViewSet.queryset.query.select_related,
            d2={'package': {}},
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PackageImageViewSet.http_method_names,
            tuple2=('get', 'post', 'delete', 'options'),
        )

    def test_get_list(self):
        # Verify that a non logged in user can see results but not 'id'
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        request = response.wsgi_request
        image = f'{request.scheme}://{request.get_host()}{self.package_image_2.image.url}'
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
                'id': str(self.package_image_2.id),
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
                'id': str(self.package_image_2.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.package_image_1.id}/'
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
        image = f'{request.scheme}://{request.get_host()}{self.package_image_1.image.url}'
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'image': image,
                'id': str(self.package_image_1.id),
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
                'id': str(self.package_image_1.id),
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
            d2={'detail': 'Invalid package_slug.'},
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
            path=self.api_path + f'{self.package_image_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete an image
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.package_image_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete an image
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.package_image_2.id}/',
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
            second=f'{self.package} - Image',
        )


class PackageTagViewSetTestCase(APITestCase):

    base_api_path = contributor = owner = package = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.package = PackageFactory(
            owner=cls.owner,
        )
        cls.base_api_path = f'/api/packages/tags/'
        cls.api_path = f'{cls.base_api_path}{cls.package.slug}/'
        cls.contributor = ForumUserFactory()
        PackageContributorFactory(
            package=cls.package,
            user=cls.contributor,
        )
        cls.package_tag_1 = PackageTagFactory(
            package=cls.package,
        )
        cls.package_tag_2 = PackageTagFactory(
            package=cls.package,
        )
        cls.regular_user = ForumUserFactory()

    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PackageTagViewSet, ProjectTagViewSet))

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageTagViewSet.serializer_class,
            second=PackageTagSerializer,
        )
        self.assertEqual(
            first=PackageTagViewSet.project_type,
            second='package',
        )
        self.assertEqual(
            first=PackageTagViewSet.project_model,
            second=Package,
        )
        self.assertIs(
            expr1=PackageTagViewSet.queryset.model,
            expr2=PackageTag,
        )
        self.assertDictEqual(
            d1=PackageTagViewSet.queryset.query.select_related,
            d2={'tag': {}, 'package': {}}
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PackageTagViewSet.http_method_names,
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
                'tag': self.package_tag_2.tag.name,
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
                'tag': self.package_tag_2.tag.name,
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
                'tag': self.package_tag_2.tag.name,
                'id': str(self.package_tag_2.id),
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
                'tag': self.package_tag_2.tag.name,
                'id': str(self.package_tag_2.id),
            },
        )

    def test_get_details(self):
        # Verify that non logged in user cannot see details
        api_path = f'{self.api_path}{self.package_tag_1.id}/'
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
                'tag': self.package_tag_1.tag.name,
                'id': str(self.package_tag_1.id),
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
                'tag': self.package_tag_1.tag.name,
                'id': str(self.package_tag_1.id),
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
            d2={'detail': 'Invalid package_slug.'},
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
            data={'tag': self.package_tag_1.tag},
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_400_BAD_REQUEST,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'tag': [f'Tag already linked to {PackageTagViewSet.project_type}.']}
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
            path=self.api_path + f'{self.package_tag_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot delete a tag
        self.client.force_login(self.regular_user.user)
        response = self.client.delete(
            path=self.api_path + f'{self.package_tag_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributor can delete a tag
        self.client.force_login(self.contributor.user)
        response = self.client.delete(
            path=self.api_path + f'{self.package_tag_1.id}/',
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_204_NO_CONTENT,
        )

        # Verify that owner can delete a tag
        self.client.force_login(self.owner.user)
        response = self.client.delete(
            path=self.api_path + f'{self.package_tag_2.id}/',
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
            second=f'{self.package} - Tag',
        )
