# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import url

# App
from .views import (
    PackageAddContributorConfirmationView, PackageAddContributorView,
    PackageCreateView, PackageEditView, PackageListView,
    PackageReleaseListView, PackageSelectGamesView, PackageUpdateView,
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
        # http://plugins.sourcepython.com/packages/<slug>/
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PackageView.as_view(),
        name='detail',
    ),
    url(
        # http://plugins.sourcepython.com/packages/<slug>/edit/
        regex=r'^(?P<slug>[\w-]+)/edit/',
        view=PackageEditView.as_view(),
        name='edit',
    ),
    url(
        # http://plugins.sourcepython.com/packages/<slug>/games/
        regex=r'^(?P<slug>[\w-]+)/games/',
        view=PackageSelectGamesView.as_view(),
        name='select-games',
    ),
    url(
        # http://plugins.sourcepython.com/packages/<slug>/releases/
        regex=r'^(?P<slug>[\w-]+)/releases/',
        view=PackageReleaseListView.as_view(),
        name='releases',
    ),
    url(
        # http://plugins.sourcepython.com/packages/<slug>/update/
        regex=r'^(?P<slug>[\w-]+)/update/',
        view=PackageUpdateView.as_view(),
        name='update',
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
