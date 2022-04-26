# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.views import APIView

# App
from project_manager.api.views import ProjectManagerAPIView


# =============================================================================
# TEST CASES
# =============================================================================
class ProjectManagerAPIViewTestCase(APITestCase):

    api_path = reverse(
        viewname='api:api-root',
    )

    def test_class_inheritance(self):
        self.assertTrue(expr=issubclass(ProjectManagerAPIView, APIView))

    def test_allowed_methods(self):
        self.assertListEqual(
            list1=ProjectManagerAPIView().allowed_methods,
            list2=['GET', 'OPTIONS'],
        )

    def test_get(self):
        response = self.client.get(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertDictEqual(
            d1=response.json(),
            d2={
                'games': reverse(
                    viewname='api:games:games-list',
                    request=response.wsgi_request,
                ),
                'packages': reverse(
                    viewname='api:packages:endpoints',
                    request=response.wsgi_request,
                ),
                'plugins': reverse(
                    viewname='api:plugins:endpoints',
                    request=response.wsgi_request,
                ),
                'sub-plugins': reverse(
                    viewname='api:sub-plugins:endpoints',
                    request=response.wsgi_request,
                ),
                'tags': reverse(
                    viewname='api:tags:tags-list',
                    request=response.wsgi_request,
                ),
                'users': reverse(
                    viewname='api:users:users-list',
                    request=response.wsgi_request,
                ),
            },
        )

    def test_options(self):
        response = self.client.options(path=self.api_path)
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['name'],
            second='Project Manager APIs',
        )
