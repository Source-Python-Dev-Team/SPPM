"""Package URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf.urls import include, url

# App
from .views import (
    PackageCreateView, PackageEditView, PackageListView,
    PackageReleaseListView, PackageSelectGamesView, PackageUpdateView,
    PackageView,
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
app_name = 'packages'

urlpatterns = [
    url(
        # /packages/
        regex=r'^$',
        view=PackageListView.as_view(),
        name='list',
    ),
    url(
        # /packages/create/
        regex=r'^create/',
        view=PackageCreateView.as_view(),
        name='create',
    ),
    url(
        # /packages/<slug>/
        regex=r'^(?P<slug>[\w-]+)/$',
        view=PackageView.as_view(),
        name='detail',
    ),
    url(
        # /packages/<slug>/edit/
        regex=r'^(?P<slug>[\w-]+)/edit/',
        view=PackageEditView.as_view(),
        name='edit',
    ),
    url(
        # /packages/<slug>/games/
        regex=r'^(?P<slug>[\w-]+)/games/',
        view=PackageSelectGamesView.as_view(),
        name='select-games',
    ),
    url(
        # /packages/<slug>/releases/
        regex=r'^(?P<slug>[\w-]+)/releases/',
        view=PackageReleaseListView.as_view(),
        name='releases',
    ),
    url(
        # /packages/<slug>/update/
        regex=r'^(?P<slug>[\w-]+)/update/',
        view=PackageUpdateView.as_view(),
        name='update',
    ),
    url(
        # /packages/<slug>/contributors/
        regex=r'^(?P<slug>[\w-]+)/contributors/',
        view=include(
            'project_manager.packages.contributors.urls',
            namespace='contributors',
        ),
    ),
]
