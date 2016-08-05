# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import include, url

# App
from .views import (
    SubPluginCreateView, SubPluginEditView, SubPluginListView,
    SubPluginReleaseListView, SubPluginSelectGamesView, SubPluginUpdateView,
    SubPluginView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        # /plugins/<slug>/sub-plugins/
        regex=r'^$',
        view=SubPluginListView.as_view(),
        name='list',
    ),
    url(
        # /plugins/<slug>/sub-plugins/create/
        regex=r'^create/',
        view=SubPluginCreateView.as_view(),
        name='create',
    ),
    url(
        # /plugins/<slug>/sub-plugins/<sub_plugin_slug>/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/$',
        view=SubPluginView.as_view(),
        name='detail',
    ),
    url(
        # /plugins/<slug>/sub-plugins/<sub_plugin_slug>/edit/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/edit/',
        view=SubPluginEditView.as_view(),
        name='edit',
    ),
    url(
        # /plugins/<slug>/sub-plugins/<sub_plugin_slug>/games/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/games/',
        view=SubPluginSelectGamesView.as_view(),
        name='select-games',
    ),
    url(
        # /plugins/<slug>/sub-plugins/<sub_plugin_slug>/releases/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/releases/',
        view=SubPluginReleaseListView.as_view(),
        name='releases',
    ),
    url(
        # /plugins/<slug>/sub-plugins/<sub_plugin_slug>/update/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/update/',
        view=SubPluginUpdateView.as_view(),
        name='update',
    ),
    url(
        # /plugins/<slug>/contributors/
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/contributors/',
        view=include(
            'project_manager.sub_plugins.contributors.urls',
            namespace='contributors',
        ),
    ),
]
