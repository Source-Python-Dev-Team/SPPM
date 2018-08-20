"""Plugin URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import include, url

# App
from project_manager.plugins.constants import UUID_RE_STRING
from project_manager.plugins.views import (
    PluginCreateView,
    PluginEditView,
    PluginListView,
    PluginReleaseListView,
    PluginSelectGamesView,
    PluginUpdateView,
    PluginView,
    SubPluginPathCreateView,
    SubPluginPathDeleteView,
    SubPluginPathEditView,
    SubPluginPathListView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
app_name = 'plugins'

urlpatterns = [
    url(
        # /plugins/
        regex=r'^$',
        view=PluginListView.as_view(),
        name='list',
    ),
    url(
        # /plugins/create/
        regex=r'^create/',
        view=PluginCreateView.as_view(),
        name='create',
    ),
    url(
        # /plugins/<slug>/
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PluginView.as_view(),
        name='detail',
    ),
    url(
        # /plugins/<slug>/edit/
        regex=r'^(?P<slug>[\w-]+)/edit/',
        view=PluginEditView.as_view(),
        name='edit',
    ),
    url(
        # /plugins/<slug>/games/
        regex=r'^(?P<slug>[\w-]+)/games/$',
        view=PluginSelectGamesView.as_view(),
        name='select-games',
    ),
    url(
        # /plugins/<slug>/releases/
        regex=r'^(?P<slug>[\w-]+)/releases/',
        view=PluginReleaseListView.as_view(),
        name='releases',
    ),
    url(
        # /plugins/<slug>/update/
        regex=r'^(?P<slug>[\w-]+)/update/',
        view=PluginUpdateView.as_view(),
        name='update',
    ),
    url(
        # /plugins/<slug>/contributors/
        regex=r'^(?P<slug>[\w-]+)/contributors/',
        view=include(
            'project_manager.plugins.contributors.urls',
            namespace='contributors',
        ),
    ),
    url(
        # /plugins/<slug>/paths/
        regex=r'^(?P<slug>[\w-]+)/paths/$',
        view=SubPluginPathListView.as_view(),
        name='path_list',
    ),
    url(
        # /plugins/<slug>/paths/create/
        regex=r'^(?P<slug>[\w-]+)/paths/create/$',
        view=SubPluginPathCreateView.as_view(),
        name='path_create',
    ),
    url(
        # /plugins/<slug>/paths/edit/<id>/
        regex=r'^(?P<slug>[\w-]+)/paths/edit/(?P<path_pk>{uuid})/'.format(
            uuid=UUID_RE_STRING,
        ),
        view=SubPluginPathEditView.as_view(),
        name='path_edit',
    ),
    url(
        # /plugins/<slug>/paths/delete/<id>/
        regex=r'^(?P<slug>[\w-]+)/paths/delete/(?P<path_pk>{uuid})/'.format(
            uuid=UUID_RE_STRING,
        ),
        view=SubPluginPathDeleteView.as_view(),
        name='path_delete',
    ),
    url(
        # /plugins/<slug>/sub-plugins/
        regex=r'^(?P<slug>[\w-]+)/sub-plugins/',
        view=include(
            'project_manager.sub_plugins.urls',
            namespace='sub-plugins',
        ),
    ),
]
