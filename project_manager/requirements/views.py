"""Requirement views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from django.views.generic import DetailView

# App
from project_manager.common.helpers import get_groups
from project_manager.common.views import PaginatedListView
from project_manager.requirements.models import PyPiRequirement


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PyPiListView',
    'PyPiView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PyPiListView(PaginatedListView):
    """PyPiRequirement listing view."""

    model = PyPiRequirement
    paginate_by = 20
    template_name = 'pypi/list.html'


class PyPiView(DetailView):
    """PyPiRequirement get view."""

    model = PyPiRequirement
    template_name = 'pypi/view.html'

    def get_context_data(self, **kwargs):
        """Add necessary context for the template."""
        context = super().get_context_data(**kwargs)
        context.update({
            'required_in_plugins': get_groups(
                self.object.required_in_plugins.all()),
            'required_in_sub_plugins': get_groups(
                self.object.required_in_subplugins.all().select_related(
                    'plugin',
                )
            ),
            'required_in_packages': get_groups(
                self.object.required_in_packages.all()),
        })
        return context
