"""Common helper functions for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
#  Django
from django.db.models import Prefetch

# App
from project_manager.packages.models import Package
from project_manager.requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'get_prefetch',
)


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def get_prefetch(release_class):
    """Return a common Prefetch for Projects."""
    return (
        Prefetch(
            lookup='releases',
            queryset=release_class.objects.order_by(
                '-created',
            ),
        ),
        Prefetch(
            lookup='package_requirements',
            queryset=Package.objects.order_by(
                'name',
            ),
        ),
        Prefetch(
            lookup='download_requirements',
            queryset=DownloadRequirement.objects.order_by(
                'name',
            ),
        ),
        Prefetch(
            lookup='pypi_requirements',
            queryset=PyPiRequirement.objects.order_by(
                'name',
            ),
        ),
        Prefetch(
            lookup='vcs_requirements',
            queryset=VersionControlRequirement.objects.order_by(
                'name',
            ),
        ),
    )
