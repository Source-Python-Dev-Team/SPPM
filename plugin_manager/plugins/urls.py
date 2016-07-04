# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import include, url

# App
from .views import (
    PluginCreateView, PluginEditView, PluginListView, PluginReleaseListView,
    PluginSelectGamesView, PluginUpdateView, PluginView,
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
        # http://plugins.sourcepython.com/plugins/<slug>/
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PluginView.as_view(),
        name='detail',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/edit/
        regex=r'^(?P<slug>[\w-]+)/edit/',
        view=PluginEditView.as_view(),
        name='edit',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/games/
        regex=r'^(?P<slug>[\w-]+)/games/$',
        view=PluginSelectGamesView.as_view(),
        name='select-games',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/releases/
        regex=r'^(?P<slug>[\w-]+)/releases/',
        view=PluginReleaseListView.as_view(),
        name='releases',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/update/
        regex=r'^(?P<slug>[\w-]+)/update/',
        view=PluginUpdateView.as_view(),
        name='update',
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/contributors/
        regex=r'^(?P<slug>[\w-]+)/contributors/',
        view=include(
            'plugin_manager.plugins.contributors.urls',
            namespace='contributors',
        ),
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/paths/
        regex=r'^(?P<slug>[\w-]+)/paths/',
        view=include(
            'plugin_manager.plugins.paths.urls',
            namespace='paths',
        ),
    ),
    url(
        # http://plugins.sourcepython.com/plugins/<slug>/sub-plugins/
        regex=r'^(?P<slug>[\w-]+)/sub-plugins/',
        view=include(
            'plugin_manager.sub_plugins.urls',
            namespace='sub-plugins',
        ),
    ),
]
