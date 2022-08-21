# =============================================================================
# IMPORTS
# =============================================================================
# Python
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
from project_manager.api.common.views import ProjectImageViewSet
from project_manager.sub_plugins.api.serializers import SubPluginImageSerializer
from project_manager.sub_plugins.api.views import SubPluginImageViewSet
from project_manager.sub_plugins.models import (
    SubPlugin,
    SubPluginImage,
)
from test_utils.factories.plugins import PluginFactory
from test_utils.factories.sub_plugins import (
    SubPluginContributorFactory,
    SubPluginFactory,
    SubPluginImageFactory,
)
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
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
