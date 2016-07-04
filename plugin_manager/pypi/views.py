# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from django.views.generic import DetailView

# App
from .models import PyPiRequirement
from plugin_manager.common.helpers import get_groups
from plugin_manager.common.views import PaginatedListView


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
    model = PyPiRequirement
    paginate_by = 20
    template_name = 'pypi/list.html'


class PyPiView(DetailView):
    model = PyPiRequirement
    template_name = 'pypi/view.html'

    def get_context_data(self, **kwargs):
        context = super(PyPiView, self).get_context_data(**kwargs)
        context.update({
            'required_in_plugins': get_groups(
                self.object.required_in_plugins.all()),
            'required_in_sub_plugins': get_groups(
                self.object.required_in_sub_plugins.all()),
            'required_in_packages': get_groups(
                self.object.required_in_packages.all()),
        })
        return context
