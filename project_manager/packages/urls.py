"""Base App URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import path

# App
from project_manager.packages.views import PackageCreateView, PackageView


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = 'packages'

urlpatterns = [
    path(
        # /packages
        route='',
        view=PackageView.as_view(),
        name='list',
    ),
    path(
        # /packages/create
        route='create',
        view=PackageCreateView.as_view(),
        name='create',
    ),
    path(
        # /packages/<slug>
        route='<slug:slug>',
        view=PackageView.as_view(),
        name='detail',
    ),
]
