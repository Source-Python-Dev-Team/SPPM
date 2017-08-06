"""User URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from .views import UserListView, UserView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        # /users/
        regex=r'^$',
        view=UserListView.as_view(),
        name='list',
    ),
    url(
        # /users/<pk>/
        regex=r'^(?P<pk>[0-9]+)/$',
        view=UserView.as_view(),
        name='detail',
    ),
]
