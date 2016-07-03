# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from .views import (
    PackageAddContributorConfirmationView, PackageAddContributorView,
    PackageCreateView, PackageEditView, PackageListView, PackageUpdateView,
    PackageView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        # http://plugins.sourcepython.com/packages/
        regex=r'^$',
        view=PackageListView.as_view(),
        name='list',
    ),
    url(
        # http://plugins.sourcepython.com/packages/create/
        regex=r'^create/',
        view=PackageCreateView.as_view(),
        name='create',
    ),
    url(
        # http://plugins.sourcepython.com/packages/edit/<slug>/
        regex=r'^edit/(?P<slug>[\w-]+)/',
        view=PackageEditView.as_view(),
        name='edit',
    ),
    url(
        # http://plugins.sourcepython.com/packages/update/<slug>/
        regex=r'^update/(?P<slug>[\w-]+)/',
        view=PackageUpdateView.as_view(),
        name='update',
    ),
    url(
        # http://plugins.sourcepython.com/packages/<slug>/
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PackageView.as_view(),
        name='detail',
    ),
    url(
        # http://plugins.sourcepython.com/packages/<slug>/add-contributor/
        regex=r'^(?P<slug>[\w-]+)/add-contributor/$',
        view=PackageAddContributorView.as_view(),
        name='add_contributor',
    ),
    url(
        # http://plugins.sourcepython.com/packages/<slug>/add-contributor/<id>/
        regex=r'^(?P<slug>[\w-]+)/add-contributor/(?P<id>\d+)/$',
        view=PackageAddContributorConfirmationView.as_view(),
        name='confirm_add_contributor',
    ),
]
