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
from project_manager.plugins.api.views import PluginAPIView


# =============================================================================
# TEST CASES
# =============================================================================
class PluginAPIViewTestCase(APITestCase):

    api_path = reverse(
        viewname='api:plugins:endpoints',
    )

    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PluginAPIView, ProjectAPIView))

    def test_base_attributes(self):
        self.assertEqual(
            first=PluginAPIView.project_type,
            second='plugin',
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=PluginAPIView.http_method_names,
            tuple2=('get', 'options'),
        )

    def test_get(self):
        response = self.client.get(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        kwargs = {
            'plugin_slug': '<plugin>',
        }
        self.assertDictEqual(
            d1=response.json(),
            d2={
                key: unquote(
                    reverse(
                        viewname=f'api:plugins:{key}-list',
                        kwargs=None if key == 'projects' else kwargs,
                        request=response.wsgi_request,
                    )
                ) for key in (
                    'contributors',
                    'games',
                    'images',
                    'paths',
                    'projects',
                    'releases',
                    'tags',
                )
            }
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(first=response.json()['name'], second='Plugin APIs')
