# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.conf.urls import url

# App Imports
from .views import (
    PackageAddContributorConfirmationView,
    PackageAddContributorView,
    PackageCreateView,
    PackageEditView,
    PackageListView,
    PackageListContributorsView,
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
        name='list',
    ),
    url(
        regex=r'^create/',
        view=PackageCreateView.as_view(),
        name='create',
    ),
    url(
        regex=r'^edit/(?P<slug>[\w-]+)/',
        view=PackageEditView.as_view(),
        name='edit',
    ),
    url(
        regex=r'^update/(?P<slug>[\w-]+)/',
        view=PackageUpdateView.as_view(),
        name='update',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PackageView.as_view(),
        name='detail',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/contributors/add/$',
        view=PackageAddContributorView.as_view(),
        name='add_contributor',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/contributors/add/(?P<id>\d+)/$',
        view=PackageAddContributorConfirmationView.as_view(),
        name='confirm_add_contributor',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/contributors/$',
        view=PackageListContributorsView.as_view(),
        name='list_contributors',
    ),
]
