from django.conf.urls import url

from .views import PyPiListView, PyPiView

urlpatterns = [
    url(
        regex=r'^$',
        view=PyPiListView.as_view(),
        name='pypi-list',
    ),
    url(
        regex=r'^(?P<package_name>.*)/$',
        view=PyPiView.as_view(),
        name='pypi-detail',
    ),
]
