# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.test import TestCase
from django.urls import reverse
from django.views.generic import TemplateView

# Third Party Django
from rest_framework import status

# App
from users.views import ForumUserView
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class ForumUserViewTestCase(TestCase):

    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(ForumUserView, TemplateView),
        )

    def test_http_method_names(self):
        self.assertTupleEqual(
            tuple1=ForumUserView.http_method_names,
            tuple2=('get', 'options'),
        )

    def test_template_name(self):
        self.assertEqual(
            first=ForumUserView.template_name,
            second='main.html',
        )

    def test_get_list(self):
        response = self.client.get(
            path=reverse(
                viewname='users:list',
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data['view']
        self.assertDictEqual(
            d1=data,
            d2={'title': 'User Listing'},
        )

    def test_get_detail(self):
        user = ForumUserFactory()
        response = self.client.get(
            path=reverse(
                viewname='users:detail',
                kwargs={
                    'pk': user.forum_id,
                }
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data['view']
        self.assertDictEqual(
            d1=data,
            d2={
                'pk': str(user.forum_id),
                'title': user.user.username,
            },
        )

    def test_detail_invalid_slug(self):
        response = self.client.get(
            path=reverse(
                viewname='users:detail',
                kwargs={
                    'pk': 1,
                }
            ),
        )
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data['view']
        self.assertDictEqual(
            d1=data,
            d2={
                'pk': '1',
                'title': 'Userid "1" not found.',
            },
        )
