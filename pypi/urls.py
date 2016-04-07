from django.conf.urls import url

from .views import PyPiListView, PyPiView

urlpatterns = [
    url(
        regex=r'^$',
        view=PyPiListView.as_view(),
        name='pypi-list',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PyPiView.as_view(),
        name='pypi-detail',
    ),
]
