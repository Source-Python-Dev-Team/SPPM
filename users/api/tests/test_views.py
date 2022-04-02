# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.test import APITestCase

# App
from test_utils.factories.users import NonAdminUserFactory, ForumUserFactory
from users.api.filtersets import ForumUserFilterSet
from users.api.ordering import ForumUserOrderingFilter
from users.api.serializers import ForumUserSerializer
from users.api.views import ForumUserViewSet


# =============================================================================
# TEST CASES
# =============================================================================
class ForumUserViewSetTestCase(APITestCase):

    api_path = '/api/users/'

    def test_filter_backends(self):
        self.assertTupleEqual(
            tuple1=ForumUserViewSet.filter_backends,
            tuple2=(ForumUserOrderingFilter, DjangoFilterBackend)
        )

    def test_filterset_class(self):
        self.assertEqual(
            first=ForumUserViewSet.filterset_class,
            second=ForumUserFilterSet,
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=ForumUserViewSet.http_method_names,
            tuple2=('get', 'options'),
        )

    def test_serializer_class(self):
        self.assertEqual(
            first=ForumUserViewSet.serializer_class,
            second=ForumUserSerializer,
        )

    def test_ordering(self):
        self.assertTupleEqual(
            tuple1=ForumUserViewSet.ordering,
            tuple2=('username',),
        )

    def test_ordering_fields(self):
        self.assertTupleEqual(
            tuple1=ForumUserViewSet.ordering_fields,
            tuple2=('forum_id', 'username'),
        )

    def test_get_list(self):
        user_1 = NonAdminUserFactory(
            username='Alfred',
        )
        forum_user_1 = ForumUserFactory(
            forum_id=1,
            user=user_1,
        )
        user_2 = NonAdminUserFactory(
            username='Zach',
        )
        forum_user_2 = ForumUserFactory(
            forum_id=2,
            user=user_2,
        )

        # Test default ordering
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=2,
        )
        for n, forum_user in enumerate([forum_user_1, forum_user_2]):
            content_user = content['results'][n]
            self.assertEqual(
                first=content_user['forum_id'],
                second=forum_user.forum_id,
            )
            self.assertEqual(
                first=content_user['username'],
                second=forum_user.user.username,
            )

        # Test alphabetized custom ordering
        response = self.client.get(path=f'{self.api_path}?ordering=username')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=2,
        )
        for n, forum_user in enumerate([forum_user_1, forum_user_2]):
            content_user = content['results'][n]
            self.assertEqual(
                first=content_user['forum_id'],
                second=forum_user.forum_id,
            )
            self.assertEqual(
                first=content_user['username'],
                second=forum_user.user.username,
            )

        # Test reverse alphabetized custom ordering
        response = self.client.get(path=f'{self.api_path}?ordering=-username')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=2,
        )
        for n, forum_user in enumerate([forum_user_2, forum_user_1]):
            content_user = content['results'][n]
            self.assertEqual(
                first=content_user['forum_id'],
                second=forum_user.forum_id,
            )
            self.assertEqual(
                first=content_user['username'],
                second=forum_user.user.username,
            )

        # Test forum_id ordering
        response = self.client.get(path=f'{self.api_path}?ordering=forum_id')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=2,
        )
        for n, forum_user in enumerate([forum_user_1, forum_user_2]):
            content_user = content['results'][n]
            self.assertEqual(
                first=content_user['forum_id'],
                second=forum_user.forum_id,
            )
            self.assertEqual(
                first=content_user['username'],
                second=forum_user.user.username,
            )

        # Test reverse forum_id ordering
        response = self.client.get(path=f'{self.api_path}?ordering=-forum_id')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=2,
        )
        for n, forum_user in enumerate([forum_user_2, forum_user_1]):
            content_user = content['results'][n]
            self.assertEqual(
                first=content_user['forum_id'],
                second=forum_user.forum_id,
            )
            self.assertEqual(
                first=content_user['username'],
                second=forum_user.user.username,
            )

    def test_get_details(self):
        user = ForumUserFactory()
        response = self.client.get(path=f'{self.api_path}{user.forum_id}/')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['forum_id'],
            second=user.forum_id,
        )
        self.assertEqual(
            first=content['username'],
            second=user.user.username,
        )

    def test_get_filter(self):
        user = ForumUserFactory()
        response = self.client.get(path=f'{self.api_path}?has_contributions=true')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=0,
        )

        response = self.client.get(path=f'{self.api_path}?has_contributions=false')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=1,
        )
        content_user = content['results'][0]
        self.assertEqual(
            first=content_user['forum_id'],
            second=user.forum_id,
        )
        self.assertEqual(
            first=content_user['username'],
            second=user.user.username,
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['name'],
            second='Forum User List',
        )
