from django.conf.urls import url

from .views import PackageCreateView, PackageListView, PackageView

urlpatterns = [
    url(
        regex=r'^$',
        view=PackageListView.as_view(),
        name='package-list',
    ),
    url(
        regex=r'^create/',
        view=PackageCreateView.as_view(),
        name='package-create',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PackageView.as_view(),
        name='package-detail',
    ),
]
