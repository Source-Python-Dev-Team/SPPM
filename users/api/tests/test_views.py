# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import connection
from django.test import override_settings

# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from test_utils.factories.packages import (
    PackageContributorFactory,
    PackageFactory,
)
from test_utils.factories.plugins import (
    PluginContributorFactory,
    PluginFactory,
)
from test_utils.factories.sub_plugins import (
    SubPluginContributorFactory,
    SubPluginFactory,
)
from test_utils.factories.users import ForumUserFactory
from users.api.filtersets import ForumUserFilterSet
from users.api.ordering import ForumUserOrderingFilter
from users.api.serializers import ForumUserRetrieveSerializer
from users.api.views import ForumUserViewSet


# =============================================================================
# TEST CASES
# =============================================================================
class ForumUserViewSetTestCase(APITestCase):

    api_path = reverse(
        viewname='api:users:users-list',
    )
    user_1 = user_2 = user_3 = None

    @classmethod
    def setUpTestData(cls):
        cls.user_1 = ForumUserFactory(
            forum_id=2,
        )
        cls.user_2 = ForumUserFactory(
            forum_id=4,
        )
        cls.user_3 = ForumUserFactory(
            forum_id=1,
        )
        cls.user_4 = ForumUserFactory(
            forum_id=3,
        )

        package_1 = PackageFactory(
            owner=cls.user_1,
        )
        package_2 = PackageFactory(
            owner=cls.user_1,
        )
        package_3 = PackageFactory(
            owner=cls.user_2,
        )
        PackageContributorFactory(
            package=package_1,
            user=cls.user_2,
        )
        PackageContributorFactory(
            package=package_1,
            user=cls.user_3,
        )
        PackageContributorFactory(
            package=package_2,
            user=cls.user_2,
        )
        PackageContributorFactory(
            package=package_3,
            user=cls.user_1,
        )
        PackageContributorFactory(
            package=package_3,
            user=cls.user_3,
        )

        plugin_1 = PluginFactory(
            owner=cls.user_2,
        )
        plugin_2 = PluginFactory(
            owner=cls.user_2,
        )
        plugin_3 = PluginFactory(
            owner=cls.user_3,
        )
        PluginContributorFactory(
            plugin=plugin_1,
            user=cls.user_3,
        )
        PluginContributorFactory(
            plugin=plugin_1,
            user=cls.user_1,
        )
        PluginContributorFactory(
            plugin=plugin_2,
            user=cls.user_3,
        )
        PluginContributorFactory(
            plugin=plugin_3,
            user=cls.user_2,
        )
        PluginContributorFactory(
            plugin=plugin_3,
            user=cls.user_1,
        )

        sub_plugin_1 = SubPluginFactory(
            owner=cls.user_3,
            plugin=plugin_1,
        )
        sub_plugin_2 = SubPluginFactory(
            owner=cls.user_3,
            plugin=plugin_1,
        )
        sub_plugin_3 = SubPluginFactory(
            owner=cls.user_1,
            plugin=plugin_1,
        )
        SubPluginContributorFactory(
            sub_plugin=sub_plugin_1,
            user=cls.user_1,
        )
        SubPluginContributorFactory(
            sub_plugin=sub_plugin_1,
            user=cls.user_2,
        )
        SubPluginContributorFactory(
            sub_plugin=sub_plugin_2,
            user=cls.user_1,
        )
        SubPluginContributorFactory(
            sub_plugin=sub_plugin_3,
            user=cls.user_3,
        )
        SubPluginContributorFactory(
            sub_plugin=sub_plugin_3,
            user=cls.user_2,
        )

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
            second=ForumUserRetrieveSerializer,
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

    @override_settings(DEBUG=True)
    def test_get_list(self):
        # Test default ordering
        response = self.client.get(path=self.api_path)
        self.assertEqual(first=len(connection.queries), second=2)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=4,
        )
        for count, forum_user in enumerate([
            self.user_1,
            self.user_2,
            self.user_3,
            self.user_4,
        ]):
            content_user = content['results'][count]
            self.assertEqual(
                first=content_user['forum_id'],
                second=forum_user.forum_id,
            )
            self.assertEqual(
                first=content_user['username'],
                second=forum_user.user.username,
            )

        # Test alphabetized custom ordering
        response = self.client.get(
            path=self.api_path,
            data={'ordering': 'username'},
        )
        self.assertEqual(first=len(connection.queries), second=2)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=4,
        )
        for count, forum_user in enumerate([
            self.user_1,
            self.user_2,
            self.user_3,
            self.user_4,
        ]):
            content_user = content['results'][count]
            self.assertEqual(
                first=content_user['forum_id'],
                second=forum_user.forum_id,
            )
            self.assertEqual(
                first=content_user['username'],
                second=forum_user.user.username,
            )

        # Test reverse alphabetized custom ordering
        response = self.client.get(
            path=self.api_path,
            data={'ordering': '-username'},
        )
        self.assertEqual(first=len(connection.queries), second=2)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=4,
        )
        for count, forum_user in enumerate([
            self.user_4,
            self.user_3,
            self.user_2,
            self.user_1,
        ]):
            content_user = content['results'][count]
            self.assertEqual(
                first=content_user['forum_id'],
                second=forum_user.forum_id,
            )
            self.assertEqual(
                first=content_user['username'],
                second=forum_user.user.username,
            )

        # Test forum_id ordering
        response = self.client.get(
            path=self.api_path,
            data={'ordering': 'forum_id'},
        )
        self.assertEqual(first=len(connection.queries), second=2)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=4,
        )
        for count, forum_user in enumerate([
            self.user_3,
            self.user_1,
            self.user_4,
            self.user_2,
        ]):
            content_user = content['results'][count]
            self.assertEqual(
                first=content_user['forum_id'],
                second=forum_user.forum_id,
            )
            self.assertEqual(
                first=content_user['username'],
                second=forum_user.user.username,
            )

        # Test reverse forum_id ordering
        response = self.client.get(
            path=self.api_path,
            data={'ordering': '-forum_id'},
        )
        self.assertEqual(first=len(connection.queries), second=2)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=4,
        )
        for count, forum_user in enumerate([
            self.user_2,
            self.user_4,
            self.user_1,
            self.user_3,
        ]):
            content_user = content['results'][count]
            self.assertEqual(
                first=content_user['forum_id'],
                second=forum_user.forum_id,
            )
            self.assertEqual(
                first=content_user['username'],
                second=forum_user.user.username,
            )

    @override_settings(DEBUG=True)
    def test_get_details(self):
        for user in (
            self.user_1,
            self.user_2,
            self.user_3,
            self.user_4,
        ):
            response = self.client.get(
                path=reverse(
                    viewname='api:users:users-detail',
                    kwargs={
                        'pk': user.forum_id,
                    }
                ),
            )
            self.assertEqual(first=len(connection.queries), second=7)
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

    @override_settings(DEBUG=True)
    def test_get_filter(self):
        response = self.client.get(
            path=self.api_path,
            data={'has_contributions': True},
        )
        self.assertEqual(first=len(connection.queries), second=2)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=3,
        )
        self.assertSetEqual(
            set1={result['forum_id'] for result in content['results']},
            set2={
                self.user_1.forum_id,
                self.user_2.forum_id,
                self.user_3.forum_id,
            }
        )

        response = self.client.get(
            path=self.api_path,
            data={'has_contributions': False},
        )
        self.assertEqual(first=len(connection.queries), second=2)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(
            first=content['count'],
            second=1,
        )
        self.assertEqual(
            first=content['results'][0]['forum_id'],
            second=self.user_4.forum_id,
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
