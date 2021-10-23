# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.test import APITestCase

# App
from test_utils.factories.users import ForumUserFactory
from users.api.filtersets import ForumUserFilterSet
from users.api.serializers import ForumUserSerializer
from users.api.views import ForumUserViewSet


# =============================================================================
# TEST CASES
# =============================================================================
class ForumUserViewSetAPITestCase(APITestCase):

    def test_filter_backends(self):
        self.assertTupleEqual(
            tuple1=ForumUserViewSet.filter_backends,
            tuple2=(OrderingFilter, DjangoFilterBackend)
        )

    def test_filter_class(self):
        self.assertEqual(
            first=ForumUserViewSet.filter_class,
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
            tuple2=('user__username',),
        )

    def test_ordering_fields(self):
        self.assertTupleEqual(
            tuple1=ForumUserViewSet.ordering_fields,
            tuple2=('forum_id', 'user__username'),
        )

    def test_get(self):
        user = ForumUserFactory()
        response = self.client.get(path='/api/users/')
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

    def test_get_filter(self):
        user = ForumUserFactory()
        response = self.client.get(path='/api/users/?has_contributions=true')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['count'],
            second=0,
        )

        response = self.client.get(path='/api/users/?has_contributions=false')
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
