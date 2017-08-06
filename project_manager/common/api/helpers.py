"""Common helper functions for APIs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
#  Django
from django.db.models import Prefetch

# App
from project_manager.games.models import Game
from project_manager.packages.models import Package
from project_manager.requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)
from project_manager.tags.models import Tag
from project_manager.users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'get_prefetch',
)


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def get_prefetch(release_class, image_class):
    """Return a common Prefetch for Projects."""
    return (
        Prefetch(
            lookup='releases',
            queryset=release_class.objects.order_by(
                '-created',
            ),
        ),
        Prefetch(
            lookup='contributors',
            queryset=ForumUser.objects.order_by(
                'username',
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
        Prefetch(
            lookup='supported_games',
            queryset=Game.objects.order_by(
                'name',
            ),
        ),
        Prefetch(
            lookup='images',
            queryset=image_class.objects.order_by(
                'image',
            ),
        ),
        Prefetch(
            lookup='tags',
            queryset=Tag.objects.order_by(
                'name',
            ),
        ),
    )
