# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.conf.urls import url

# App Imports
from .views import (
    PackageCreateView,
    PackageEditView,
    PackageListView,
    PackageUpdateView,
    PackageView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^$',
        view=PackageListView.as_view(),
        name='package_list',
    ),
    url(
        regex=r'^create/',
        view=PackageCreateView.as_view(),
        name='package_create',
    ),
    url(
        regex=r'^edit/(?P<slug>[\w-]+)/',
        view=PackageEditView.as_view(),
        name='package_edit',
    ),
    url(
        regex=r'^update/(?P<slug>[\w-]+)/',
        view=PackageUpdateView.as_view(),
        name='package_update',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PackageView.as_view(),
        name='package_detail',
    ),
]
