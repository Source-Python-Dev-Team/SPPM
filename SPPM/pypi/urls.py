# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.conf.urls import url

# App Imports
from .views import PyPiListView, PyPiView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^$',
        view=PyPiListView.as_view(),
        name='list',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PyPiView.as_view(),
        name='detail',
    ),
]
