""""""

# =============================================================================
# IMPORTS
# =============================================================================
# App
from project_manager.packages.helpers import get_package_basename
from project_manager.packages.models import Package


# =============================================================================
# >> MIXINS
# =============================================================================
class PackageReleaseBase(object):
    """Serializer for listing Package releases."""

    project_class = Package
    project_type = 'package'

    @property
    def zip_parser(self):
        return get_package_basename

    def get_project_kwargs(self, parent_project=None):
        """Return kwargs for the project."""
        return {
            'pk': self.context['view'].kwargs.get('package_slug')
        }
