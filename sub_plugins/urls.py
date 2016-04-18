# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.conf.urls import url

# App Imports
from .views import (
    SubPluginAddContributorConfirmationView,
    SubPluginAddContributorsView,
    SubPluginCreateView,
    SubPluginEditView,
    SubPluginListView,
    SubPluginUpdateView,
    SubPluginView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^$',
        view=SubPluginListView.as_view(),
        name='list',
    ),
    url(
        regex=r'^create/',
        view=SubPluginCreateView.as_view(),
        name='create',
    ),
    url(
        regex=r'^edit/(?P<sub_plugin_slug>[\w-]+)/',
        view=SubPluginEditView.as_view(),
        name='edit',
    ),
    url(
        regex=r'^update/(?P<sub_plugin_slug>[\w-]+)/',
        view=SubPluginUpdateView.as_view(),
        name='update',
    ),
    url(
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/$',
        view=SubPluginView.as_view(),
        name='detail',
    ),
    url(
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/contributors/add/$',
        view=SubPluginAddContributorsView.as_view(),
        name='add_contributor',
    ),
    url(
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/contributors/add/(?P<id>\d+)/$',
        view=SubPluginAddContributorConfirmationView.as_view(),
        name='confirm_add_contributor',
    ),
]
