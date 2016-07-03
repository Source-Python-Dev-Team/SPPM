# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from .views import (
    SubPluginAddContributorConfirmationView, SubPluginAddContributorView,
    SubPluginCreateView, SubPluginEditView, SubPluginListView,
    SubPluginReleaseListView, SubPluginUpdateView, SubPluginView,
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
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/edit/<sub_plugin_slug>/
        regex=r'^edit/(?P<sub_plugin_slug>[\w-]+)/',
        view=SubPluginEditView.as_view(),
        name='edit',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/update/<sub_plugin_slug>/
        regex=r'^update/(?P<sub_plugin_slug>[\w-]+)/',
        view=SubPluginUpdateView.as_view(),
        name='update',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/<sub_plugin_slug>/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/$',
        view=SubPluginView.as_view(),
        name='detail',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/<sub_plugin_slug>/releases/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/releases/',
        view=SubPluginReleaseListView.as_view(),
        name='releases',
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
