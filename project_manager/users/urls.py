"""User URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from project_manager.users.views import UserListView, UserView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
app_name = 'users'

urlpatterns = [
    url(
        # /users/
        regex=r'^$',
        view=UserListView.as_view(),
        name='list',
    ),
    url(
        # /users/<forum_id>/
        regex=r'^(?P<pk>[0-9]+)/$',
        view=UserView.as_view(),
        name='detail',
    ),
]
