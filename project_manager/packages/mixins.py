"""Mixins for use with Packages."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# App
from .models import Package


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'RetrievePackageMixin',
)


# =============================================================================
# >> MIX-INS
# =============================================================================
class RetrievePackageMixin:
    """Mixin to retrieve the Package for the view."""

    _package = None

    @property
    def package(self):
        """Return the Package for the view."""
        if self._package is None:
            self._package = Package.objects.get(slug=self.kwargs['slug'])
        return self._package
