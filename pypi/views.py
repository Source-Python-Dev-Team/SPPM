from django.views.generic import DetailView, ListView

from .models import PyPiRequirement


__all__ = (
    'PyPiListView',
    'PyPiView',
)


class PyPiListView(ListView):
    model = PyPiRequirement
    paginate_by = 20
    template_name = 'pypi/pypi_list.html'


class PyPiView(DetailView):
    model = PyPiRequirement
    template_name = 'pypi/pypi_view.html'

    def get_context_data(self, **kwargs):
        context = super(PyPiView, self).get_context_data(**kwargs)
        context.update({
            'required_in_plugins': self.object.required_in_plugins.all(),
            'required_in_sub_plugins': self.object.required_in_sub_plugins.all(),
            'required_in_packages': self.object.required_in_packages.all(),
        })
        return context
