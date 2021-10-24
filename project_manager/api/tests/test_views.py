# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# App


# =============================================================================
# TEST CASES
# =============================================================================
class ProjectManagerAPIViewAPITestCase(APITestCase):

    def test_get(self):
        response = self.client.get(path='/api/')
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
        response = self.client.options(path='/api/')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        self.assertEqual(
            first=response.json()['name'],
            second='Project Manager APIs',
        )
