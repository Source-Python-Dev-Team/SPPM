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
from project_manager.packages.api.views import PackageAPIView


# =============================================================================
# TEST CASES
# =============================================================================
class PackageAPIViewTestCase(APITestCase):

    api_path = reverse(
        viewname='api:packages:endpoints',
    )

    def test_inheritance(self):
        self.assertTrue(expr=issubclass(PackageAPIView, ProjectAPIView))

    def test_base_attributes(self):
        self.assertEqual(
            first=PackageAPIView.project_type,
            second='package',
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=ProjectAPIView.http_method_names,
            tuple2=('get', 'options'),
        )

    def test_get(self):
        response = self.client.get(path=self.api_path)
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        kwargs = {
            'package_slug': '<package>',
        }
        self.assertDictEqual(
            d1=response.json(),
            d2={
                key: unquote(
                    reverse(
                        viewname=f'api:packages:{key}-list',
                        kwargs=None if key == 'projects' else kwargs,
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
        self.assertEqual(first=response.json()['name'], second='Package APIs')
