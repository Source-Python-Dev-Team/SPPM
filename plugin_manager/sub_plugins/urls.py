# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from .views import (
    SubPluginAddContributorConfirmationView, SubPluginAddContributorView,
    SubPluginCreateView, SubPluginEditView, SubPluginListView,
    SubPluginReleaseListView, SubPluginSelectGamesView, SubPluginUpdateView,
    SubPluginView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/
        regex=r'^$',
        view=SubPluginListView.as_view(),
        name='list',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/create/
        regex=r'^create/',
        view=SubPluginCreateView.as_view(),
        name='create',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/<sub_plugin_slug>/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/$',
        view=SubPluginView.as_view(),
        name='detail',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/<sub_plugin_slug>/edit/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/edit/',
        view=SubPluginEditView.as_view(),
        name='edit',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/<sub_plugin_slug>/games/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/games/',
        view=SubPluginSelectGamesView.as_view(),
        name='select-games',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/<sub_plugin_slug>/releases/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/releases/',
        view=SubPluginReleaseListView.as_view(),
        name='releases',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/<sub_plugin_slug>/update/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/update/',
        view=SubPluginUpdateView.as_view(),
        name='update',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/<sub_plugin_slug>/add-contributor/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/add-contributor/$',
        view=SubPluginAddContributorView.as_view(),
        name='add_contributor',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/<sub_plugin_slug>/add-contributor/<id>/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/add-contributor/(?P<id>\d+)/$',
        view=SubPluginAddContributorConfirmationView.as_view(),
        name='confirm_add_contributor',
    ),
]
