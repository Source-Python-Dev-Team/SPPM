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
        name='plugin-list',
    ),
    url(
        regex=r'^create/',
        view=PluginCreateView.as_view(),
        name='plugin-create',
    ),
    url(
        regex=r'^update/(?P<slug>[\w-]+)/',
        view=PluginUpdateView.as_view(),
        name='plugin-update',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/sub-plugins/',
        view=include(
            'sub_plugins.urls',
            namespace='sub-plugins',
        )
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PluginView.as_view(),
        name='plugin-detail',
    ),
]
