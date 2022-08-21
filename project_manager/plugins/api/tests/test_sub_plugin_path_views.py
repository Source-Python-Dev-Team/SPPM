# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.api.common.views.mixins import ProjectRelatedInfoMixin
from project_manager.plugins.api.serializers import SubPluginPathSerializer
from project_manager.plugins.api.views import SubPluginPathViewSet
from project_manager.plugins.models import (
    Plugin,
    SubPluginPath,
)
from test_utils.factories.plugins import (
    PluginContributorFactory,
    PluginFactory,
    SubPluginPathFactory,
)
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
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
            expr=issubclass(SubPluginPathViewSet, ProjectRelatedInfoMixin),
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
        # Verify that non-logged-in user cannot POST
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.plugin} - Sub-Plugin Path',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot POST
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.plugin} - Sub-Plugin Path',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can POST
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.list_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.plugin} - Sub-Plugin Path',
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
            second=f'{self.plugin} - Sub-Plugin Path',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(set1=set(content['actions']), set2={'POST'})

    def test_options_object(self):
        # Verify that non-logged-in user cannot DELETE/PATCH
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.plugin} - Sub-Plugin Path',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that normal user cannot DELETE/PATCH
        self.client.force_login(user=self.regular_user.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.plugin} - Sub-Plugin Path',
        )
        self.assertNotIn(member='actions', container=content)

        # Verify that contributors can DELETE/PATCH
        self.client.force_login(user=self.contributor.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.plugin} - Sub-Plugin Path',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(
            set1=set(content['actions']),
            set2={'DELETE', 'PATCH'},
        )

        # Verify that the owner can DELETE/PATCH
        self.client.force_login(user=self.owner.user)
        response = self.client.options(path=self.detail_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(
            first=content['name'],
            second=f'{self.plugin} - Sub-Plugin Path',
        )
        self.assertIn(member='actions', container=content)
        self.assertSetEqual(
            set1=set(content['actions']),
            set2={'DELETE', 'PATCH'},
        )
