from django.conf.urls import url

from .views import SubPluginListView, SubPluginCreateView, SubPluginView

urlpatterns = [
    url(
        regex=r'^$',
        view=SubPluginListView.as_view(),
        name='sub-plugin-list',
    ),
    url(
        regex=r'^create/',
        view=SubPluginCreateView.as_view(),
        name='sub-plugin-create',
    ),
    url(
        regex=r'^(?P<sub_plugin_name>.*)/$',
        view=SubPluginView.as_view(),
        name='sub-plugin-detail',
    ),
]
