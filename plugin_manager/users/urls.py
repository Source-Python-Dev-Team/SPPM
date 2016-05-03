# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.conf.urls import url

# App Imports
from .views import UserListView, UserView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^$',
        view=UserListView.as_view(),
        name='list',
    ),
    url(
        regex=r'^(?P<pk>[0-9]+)/$',
        view=UserView.as_view(),
        name='detail',
    ),
]
