from django.conf.urls import include, url

from .views import PluginListView, PluginCreateView, PluginView

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
        regex=r'^(?P<plugin_name>.*)/sub_plugins/',
        view=include(
            'sub_plugins.urls',
            namespace='sub_plugins',
        )
    ),
    url(
        regex=r'^(?P<plugin_name>.*)/$',
        view=PluginView.as_view(),
        name='plugin-detail',
    ),
]
