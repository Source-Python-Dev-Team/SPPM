"""Package app config."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.apps import AppConfig


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageConfig',
)


# =============================================================================
# >> APPLICATION CONFIG
# =============================================================================
class PackageConfig(AppConfig):
    """Package app config."""

    name = 'project_manager.packages'
    verbose_name = 'Packages'
