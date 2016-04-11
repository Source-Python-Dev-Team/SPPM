from django.conf.urls import include, url

from .views import (
    PluginCreateView,
    PluginEditView,
    PluginListView,
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
        regex=r'^edit/(?P<slug>[\w-]+)/',
        view=PluginEditView.as_view(),
        name='plugin_edit',
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
