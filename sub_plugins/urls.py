# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.conf.urls import url

# App Imports
from .views import (
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
        name='sub_plugin_list',
    ),
    url(
        regex=r'^create/',
        view=SubPluginCreateView.as_view(),
        name='sub_plugin_create',
    ),
    url(
        regex=r'^edit/(?P<sub_plugin_slug>[\w-]+)/',
        view=SubPluginEditView.as_view(),
        name='sub_plugin_edit',
    ),
    url(
        regex=r'^update/(?P<sub_plugin_slug>[\w-]+)/',
        view=SubPluginUpdateView.as_view(),
        name='sub_plugin_update',
    ),
    url(
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/$',
        view=SubPluginView.as_view(),
        name='sub_plugin_detail',
    ),
]
