# =============================================================================
# IMPORTS
# =============================================================================
# Python
import tempfile
from datetime import timedelta

# Django
from django.db import connection
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
from project_manager.api.common.views import ProjectImageViewSet
from project_manager.plugins.api.serializers import PluginImageSerializer
from project_manager.plugins.api.views import PluginImageViewSet
from project_manager.plugins.models import (
    Plugin,
    PluginImage,
)
from test_utils.factories.plugins import (
    PluginContributorFactory,
    PluginFactory,
    PluginImageFactory,
)
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class PluginImageViewSetTestCase(APITestCase):

    contributor = detail_api = list_api = owner = plugin_1 = plugin_2 = None
    plugin_image_1 = None
    MEDIA_ROOT = Path(tempfile.mkdtemp())

    @classmethod
    def setUpTestData(cls):
        cls.owner = ForumUserFactory()
        cls.plugin_1 = PluginFactory(
            owner=cls.owner,
        )
        cls.plugin_2 = PluginFactory(
            owner=cls.owner,
        )
        cls.contributor = ForumUserFactory()
        PluginContributorFactory(
            plugin=cls.plugin_1,
            user=cls.contributor,
        )
        PluginContributorFactory(
            plugin=cls.plugin_2,
            user=cls.contributor,
        )
        cls.plugin_image_1 = PluginImageFactory(
            plugin=cls.plugin_1,
        )
        cls.plugin_image_2 = PluginImageFactory(
            plugin=cls.plugin_1,
            created=now() + timedelta(minutes=1)
        )
        cls.regular_user = ForumUserFactory()
        cls.detail_api = 'api:plugins:images-detail'
        cls.list_api = 'api:plugins:images-list'
        cls.detail_path = reverse(
            viewname=cls.detail_api,
            kwargs={
                'plugin_slug': cls.plugin_1.slug,
                'pk': cls.plugin_image_1.id,
            },
        )
        cls.list_path = reverse(
            viewname=cls.list_api,
            kwargs={
                'plugin_slug': cls.plugin_1.slug,
            },
        )

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

    @override_settings(DEBUG=True)
    def test_get_list(self):
        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=self.list_path)
        self.assertEqual(first=len(connection.queries), second=4)
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
        self.assertEqual(first=len(connection.queries), second=6)
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
        self.assertEqual(first=len(connection.queries), second=6)
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
        self.assertEqual(first=len(connection.queries), second=5)
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

    @override_settings(DEBUG=True)
    def test_get_list_empty(self):
        list_path = reverse(
            viewname=self.list_api,
            kwargs={
                'plugin_slug': self.plugin_2.slug,
            },
        )

        # Verify that non-logged-in user can see results but not 'id'
        response = self.client.get(path=list_path)
        self.assertEqual(first=len(connection.queries), second=2)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(first=response.json()['count'], second=0)

        # Verify that regular user can see results but not 'id'
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=list_path)
        self.assertEqual(first=len(connection.queries), second=4)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(first=response.json()['count'], second=0)

        # Verify that contributors can see results AND 'id'
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=list_path)
        self.assertEqual(first=len(connection.queries), second=4)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(first=response.json()['count'], second=0)

        # Verify that the owner can see results AND 'id'
        self.client.force_login(self.owner.user)
        response = self.client.get(path=list_path)
        self.assertEqual(first=len(connection.queries), second=4)
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
                    'plugin_slug': 'invalid',
                }
            ),
        )
        self.assertEqual(first=len(connection.queries), second=1)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_404_NOT_FOUND,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={'detail': 'Invalid plugin_slug.'},
        )

    @override_settings(DEBUG=True)
    def test_get_details(self):
        # Verify that non-logged-in user cannot see details
        response = self.client.get(path=self.detail_path)
        self.assertEqual(first=len(connection.queries), second=3)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that regular user cannot see details
        self.client.force_login(self.regular_user.user)
        response = self.client.get(path=self.detail_path)
        self.assertEqual(first=len(connection.queries), second=5)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_403_FORBIDDEN,
        )

        # Verify that contributors can see details
        self.client.force_login(self.contributor.user)
        response = self.client.get(path=self.detail_path)
        self.assertEqual(first=len(connection.queries), second=5)
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
        self.assertEqual(first=len(connection.queries), second=5)
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

    @override_settings(DEBUG=True)
    def test_get_detail_failure(self):
        self.client.force_login(self.owner.user)
        response = self.client.get(
            path=reverse(
                viewname=self.detail_api,
                kwargs={
                    'plugin_slug': self.plugin_1.slug,
                    'pk': 'invalid',
                },
            ),
        )
        self.assertEqual(first=len(connection.queries), second=3)
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
        # Verify that non-logged-in user cannot add an image
        image = Image.new('RGB', (100, 100))
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp_file:
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
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp_file:
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
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp_file:
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
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp_file:
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
        # Verify that non-logged-in user cannot delete an image
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
                    'plugin_slug': self.plugin_1.slug,
                    'pk': self.plugin_image_2.id,
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
            second=f'{self.plugin_1} - Image',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot POST
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.plugin_1} - Image',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can POST
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.plugin_1} - Image',
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
            second=f'{self.plugin_1} - Image',
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
            second=f'{self.plugin_1} - Image',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot DELETE
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.plugin_1} - Image',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can DELETE
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.plugin_1} - Image',
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
            second=f'{self.plugin_1} - Image',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'DELETE'})
