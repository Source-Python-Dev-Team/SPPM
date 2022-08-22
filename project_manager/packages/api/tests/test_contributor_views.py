# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db import connection, reset_queries
from django.test import override_settings

# Third Party Django
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.api.common.views import ProjectContributorViewSet
from project_manager.packages.api.serializers import PackageContributorSerializer
from project_manager.packages.api.views import PackageContributorViewSet
from project_manager.packages.models import (
    Package,
    PackageContributor,
)
from test_utils.factories.packages import (
    PackageFactory,
    PackageContributorFactory,
)
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PackageContributorViewSetTestCase(APITestCase):

    contributor = detail_api = list_api = owner = package_1 = None
    package_contributor = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.package_1 = PackageFactory(
            owner=cls.owner,
        )
        cls.package_2 = PackageFactory(
            owner=cls.owner,
        )
        cls.contributor = ForumUserFactory()
        cls.package_contributor = PackageContributorFactory(
            package=cls.package_1,
            user=cls.contributor,
        )
        PackageContributorFactory(
            package=cls.package_1,
        )
        cls.new_contributor = ForumUserFactory()
        cls.regular_user = ForumUserFactory()
        cls.detail_api = 'api:packages:contributors-detail'
        cls.list_api = 'api:packages:contributors-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'package_slug': cls.package_1.slug,
                'pk': cls.package_contributor.id,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'package_slug': cls.package_1.slug,
            },
        )

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

    @override_settings(DEBUG=True)
    def test_get_list(self):
        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=self.list_path)
        self.assertEqual(
            first=len(connection.queries),
            second=4,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'user': {
                    'forum_id': self.contributor.forum_id,
                    'username': self.contributor.user.username,
                },
            },
        )

        # Verify that regular user can see results but not 'id'
        reset_queries()
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.list_path)
        self.assertEqual(
            first=len(connection.queries),
            second=6,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'user': {
                    'forum_id': self.contributor.forum_id,
                    'username': self.contributor.user.username,
                },
            },
        )

        # Verify that contributors can see results but not 'id'
        reset_queries()
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.list_path)
        self.assertEqual(
            first=len(connection.queries),
            second=6,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'user': {
                    'forum_id': self.contributor.forum_id,
                    'username': self.contributor.user.username,
                },
            },
        )

        # Verify that the owner can see results AND 'id'
        reset_queries()
        self.client.force_login(self.owner.user)
        response = self.client.get(path=self.list_path)
        self.assertEqual(
            first=len(connection.queries),
            second=5,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        content = response.json()
        self.assertEqual(first=content['count'], second=2)
        self.assertDictEqual(
            d1=content['results'][0],
            d2={
                'user': {
                    'forum_id': self.contributor.forum_id,
                    'username': self.contributor.user.username,
                },
                'id': str(self.package_contributor.id),
            },
        )

    @override_settings(DEBUG=True)
    def test_get_list_empty(self):
        list_path = reverse(
            viewname=self.list_api,
            kwargs={
                'package_slug': self.package_2.slug,
            },
        )

        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=list_path)
        self.assertEqual(
            first=len(connection.queries),
            second=2,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(first=response.json()['count'], second=0)

        # Verify that regular user can see results but not 'id'
        reset_queries()
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=list_path)
        self.assertEqual(
            first=len(connection.queries),
            second=4,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(first=response.json()['count'], second=0)

        # Verify that the owner can see results AND 'id'
        reset_queries()
        self.client.force_login(self.owner.user)
        response = self.client.get(path=list_path)
        self.assertEqual(
            first=len(connection.queries),
            second=4,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(first=response.json()['count'], second=0)

    @override_settings(DEBUG=True)
    def test_get_list_failure(self):
        response = self.client.get(
            path=reverse(
                viewname=self.list_api,
                kwargs={
                    'package_slug': 'invalid',
                },
            ),
        )
        self.assertEqual(
            first=len(connection.queries),
            second=1,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid package_slug.'},
        )

    @override_settings(DEBUG=True)
    def test_get_details(self):
        # Verify that non-logged-in user cannot see details
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=len(connection.queries),
            second=3,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot see details
        reset_queries()
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=len(connection.queries),
            second=5,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributors cannot see details
        reset_queries()
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=len(connection.queries),
            second=5,
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that the owner can see details
        reset_queries()
        self.client.force_login(self.owner.user)
        response = self.client.get(path=self.detail_path)
        self.assertEqual(
            first=len(connection.queries),
            second=5,
        )
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

    @override_settings(DEBUG=True)
    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'package_slug': self.package_1.slug,
                    'pk': 'invalid',
                },
            ),
        )
        self.assertEqual(
            first=len(connection.queries),
            second=3,
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
            second=f'{self.package_1} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot POST
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.package_1} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors cannot POST
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.package_1} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that the owner can POST
        self.client.force_login(user=self.owner.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.package_1} - Contributor',
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
            second=f'{self.package_1} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot DELETE
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.package_1} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors cannot DELETE
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.package_1} - Contributor',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that the owner can DELETE
        self.client.force_login(user=self.owner.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.package_1} - Contributor',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'DELETE'})
