# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from .views import PyPiListView, PyPiView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        # /pypi/
        regex=r'^$',
        view=PyPiListView.as_view(),
        name='list',
    ),
    url(
        # /pypi/<slug>/
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PyPiView.as_view(),
        name='detail',
    ),
]
