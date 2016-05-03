# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.conf.urls import include, url

# App Imports
from .views import (
    PluginAddContributorConfirmationView,
    PluginAddContributorView,
    PluginCreateView,
    PluginEditView,
    PluginListView,
    PluginUpdateView,
    PluginView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^$',
        view=PluginListView.as_view(),
        name='list',
    ),
    url(
        regex=r'^create/',
        view=PluginCreateView.as_view(),
        name='create',
    ),
    url(
        regex=r'^edit/(?P<slug>[\w-]+)/',
        view=PluginEditView.as_view(),
        name='edit',
    ),
    url(
        regex=r'^update/(?P<slug>[\w-]+)/',
        view=PluginUpdateView.as_view(),
        name='update',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/sub-plugins/',
        view=include(
            'SPPM.sub_plugins.urls',
            namespace='sub_plugins',
        ),
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PluginView.as_view(),
        name='detail',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/add-contributor/$',
        view=PluginAddContributorView.as_view(),
        name='add_contributor',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/add-contributor/(?P<id>\d+)/$',
        view=PluginAddContributorConfirmationView.as_view(),
        name='confirm_add_contributor',
    ),
]
