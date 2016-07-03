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
        # http://plugins.sourcepython.com/users/
        regex=r'^$',
        view=UserListView.as_view(),
        name='list',
    ),
    url(
        # http://plugins.sourcepython.com/users/<pk>/
        regex=r'^(?P<pk>[0-9]+)/$',
        view=UserView.as_view(),
        name='detail',
    ),
]
