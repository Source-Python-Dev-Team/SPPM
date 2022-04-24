# =============================================================================
# IMPORTS
# =============================================================================
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

    api_path = '/api/plugins/'

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
        base_path = reverse(
            viewname=f'api:plugins:endpoints',
            request=response.wsgi_request,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'contributors': base_path + f'contributors/<plugin>/',
                'games': base_path + f'games/<plugin>/',
                'images': base_path + f'images/<plugin>/',
                'projects': base_path + f'projects/',
                'releases': base_path + f'releases/<plugin>/',
                'tags': base_path + f'tags/<plugin>/',
                'paths': base_path + f'paths/<plugin>/',
            }
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(first=response.json()['name'], second='Plugin APIs')
