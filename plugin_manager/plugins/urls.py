# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import include, url

# App
from .views import (
    PluginAddContributorConfirmationView, PluginAddContributorView,
    PluginCreateView, PluginEditView, PluginListView, PluginUpdateView,
    PluginView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        # http://plugins.sourcepython.com/plugins/
        regex=r'^$',
        view=PluginListView.as_view(),
        name='list',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/create/
        regex=r'^create/',
        view=PluginCreateView.as_view(),
        name='create',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/edit/<slug>/
        regex=r'^edit/(?P<slug>[\w-]+)/',
        view=PluginEditView.as_view(),
        name='edit',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/update/<slug>/
        regex=r'^update/(?P<slug>[\w-]+)/',
        view=PluginUpdateView.as_view(),
        name='update',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PluginView.as_view(),
        name='detail',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/
        regex=r'^(?P<slug>[\w-]+)/sub-plugins/',
        view=include(
            'plugin_manager.sub_plugins.urls',
            namespace='sub_plugins',
        ),
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/add-contributor/
        regex=r'^(?P<slug>[\w-]+)/add-contributor/$',
        view=PluginAddContributorView.as_view(),
        name='add_contributor',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/add-contributor/<id>/
        regex=r'^(?P<slug>[\w-]+)/add-contributor/(?P<id>\d+)/$',
        view=PluginAddContributorConfirmationView.as_view(),
        name='confirm_add_contributor',
    ),
]
