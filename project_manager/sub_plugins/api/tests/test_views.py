# =============================================================================
# IMPORTS
# =============================================================================
# Python
from urllib.parse import unquote

# Third Party Django
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App
from project_manager.api.common.views import ProjectAPIView
from project_manager.sub_plugins.api.views import SubPluginAPIView


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginAPIViewTestCase(APITestCase):

    api_path = reverse(
        viewname='api:sub-plugins:endpoints',
    )

    def test_inheritance(self):
        self.assertTrue(expr=issubclass(SubPluginAPIView, ProjectAPIView))

    def test_base_attributes(self):
        self.assertEqual(
            first=SubPluginAPIView.project_type,
            second='sub-plugin',
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=SubPluginAPIView.http_method_names,
            tuple2=('get', 'options'),
        )

    def test_get(self):
        response = self.client.get(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        base_kwargs = {
            'plugin_slug': '<plugin>',
        }
        kwargs = {
            'sub_plugin_slug': '<sub-plugin>',
            **base_kwargs,
        }
        self.assertDictEqual(
            d1=response.json(),
            d2={
                key: unquote(
                    reverse(
                        viewname=f'api:sub-plugins:{key}-list',
                        kwargs=base_kwargs if key == 'projects' else kwargs,
                        request=response.wsgi_request,
                    )
                ) for key in (
                    'contributors',
                    'games',
                    'images',
                    'projects',
                    'releases',
                    'tags',
                )
            }
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(first=response.json()['name'], second='Sub-Plugin APIs')
