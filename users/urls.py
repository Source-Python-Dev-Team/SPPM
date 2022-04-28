"""User URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import path

# App
from users.views import ForumUserView


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'users'

urlpatterns = [
    path(
        # /users
        route='',
        view=ForumUserView.as_view(),
        name='list',
    ),
    path(
        # /users/<pk>
        route='<pk>',
        view=ForumUserView.as_view(),
        name='detail',
    ),
]
