"""Mixins for package functionalities between APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# App
from project_manager.packages.helpers import PackageZipFile
from project_manager.packages.models import Package


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageReleaseBase',
)


# =============================================================================
# MIXINS
# =============================================================================
class PackageReleaseBase:
    """Serializer for listing Package releases."""

    project_class = Package
    project_type = 'package'

    @property
    def zip_parser(self):
        """Return the Package zip parsing function."""
        return PackageZipFile

    def get_project_kwargs(self):
        """Return kwargs for the project."""
        return {
            'pk': getattr(self, 'context')['view'].kwargs.get('package_slug')
        }
