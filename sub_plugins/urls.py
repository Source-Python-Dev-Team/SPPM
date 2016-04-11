from django.conf.urls import url

from .views import (
    SubPluginListView,
    SubPluginCreateView,
    SubPluginUpdateView,
    SubPluginView,
)

urlpatterns = [
    url(
        regex=r'^$',
        view=SubPluginListView.as_view(),
        name='sub_plugin_list',
    ),
    url(
        regex=r'^create/',
        view=SubPluginCreateView.as_view(),
        name='sub_plugin_create',
    ),
    url(
        regex=r'^update/(?P<sub_plugin_slug>[\w-]+)/',
        view=SubPluginUpdateView.as_view(),
        name='sub_plugin_update',
    ),
    url(
        regex=r'^(?P<sub_plugin_slug>[\w-]+)/$',
        view=SubPluginView.as_view(),
        name='sub_plugin_detail',
    ),
]
