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
        name='user_list',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=UserView.as_view(),
        name='user_detail',
    ),
]
