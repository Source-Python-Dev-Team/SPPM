from django.conf.urls import include, url

from .views import (
    PluginListView,
    PluginCreateView,
    PluginUpdateView,
    PluginView,
)

urlpatterns = [
    url(
        regex=r'^$',
        view=PluginListView.as_view(),
        name='plugin_list',
    ),
    url(
        regex=r'^create/',
        view=PluginCreateView.as_view(),
        name='plugin_create',
    ),
    url(
        regex=r'^update/(?P<slug>[\w-]+)/',
        view=PluginUpdateView.as_view(),
        name='plugin_update',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/sub-plugins/',
        view=include(
            'sub_plugins.urls',
            namespace='sub_plugins',
        ),
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PluginView.as_view(),
        name='plugin_detail',
    ),
]
