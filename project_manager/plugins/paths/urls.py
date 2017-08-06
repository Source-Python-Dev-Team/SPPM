"""SubPluginPath URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from .views import (
    SubPluginPathCreateView, SubPluginPathDeleteView, SubPluginPathEditView,
    SubPluginPathListView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        # /plugins/<slug>/paths/
        regex=r'^$',
        view=SubPluginPathListView.as_view(),
        name='list',
    ),
    url(
        # /plugins/<slug>/paths/create/
        regex=r'^create/$',
        view=SubPluginPathCreateView.as_view(),
        name='create',
    ),
    url(
        # /plugins/<slug>/paths/edit/<path_pk>/
        regex=r'^edit/(?P<path_pk>[0-9]+)/',
        view=SubPluginPathEditView.as_view(),
        name='edit',
    ),
    url(
        # /plugins/<slug>/paths/delete/<path_pk>/
        regex=r'^delete/(?P<path_pk>\d+)/',
        view=SubPluginPathDeleteView.as_view(),
        name='delete',
    ),
    # url(
    #     # /plugins/<slug>/paths/delete/<path_pk>/confirmation/
    #     regex=r'^delete/(?P<path_pk>[0-9]+)/confirmation/$',
    #     view=,
    #     name='delete-confirm',
    # ),
]
