# =============================================================================
# IMPORTS
# =============================================================================
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

    api_path = '/api/sub-plugins/'

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
        base_path = reverse(
            viewname=f'api:sub-plugins:endpoints',
            request=response.wsgi_request,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'contributors': base_path + f'contributors/<plugin>/<sub-plugin>/',
                'games': base_path + f'games/<plugin>/<sub-plugin>/',
                'images': base_path + f'images/<plugin>/<sub-plugin>/',
                'projects': base_path + f'projects/<plugin>/',
                'releases': base_path + f'releases/<plugin>/<sub-plugin>/',
                'tags': base_path + f'tags/<plugin>/<sub-plugin>/',
            }
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertEqual(first=response.json()['name'], second='Sub-Plugin APIs')
