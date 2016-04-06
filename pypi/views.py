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
    slug_url_kwarg = 'package_name'
    slug_field = 'name'
