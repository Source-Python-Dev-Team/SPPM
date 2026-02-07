"""Package URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.urls import path

# App
from project_manager.packages.views import (
    PackageCreateView,
    PackageEditView,
    PackageUpdateView,
    PackageView,
)

# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
app_name = "packages"

urlpatterns = [
    path(
        # /packages
        route="",
        view=PackageView.as_view(),
        name="list",
    ),
    path(
        # /packages/create
        route="create",
        view=PackageCreateView.as_view(),
        name="create",
    ),
    path(
        # /packages/<slug>/edit
        route="<slug:slug>/edit",
        view=PackageEditView.as_view(),
        name="edit",
    ),
    path(
        # /packages/<slug>/update
        route="<slug:slug>/update",
        view=PackageUpdateView.as_view(),
        name="update",
    ),
    path(
        # /packages/<slug>
        route="<slug:slug>/",
        view=PackageView.as_view(),
        name="detail",
    ),
]
