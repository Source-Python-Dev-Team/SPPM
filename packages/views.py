from django.views.generic import CreateView, DetailView, ListView

from .models import Package
from .forms import PackageCreateForm


__all__ = (
    'PackageCreateView',
    'PackageListView',
    'PackageView',
)


# Create your views here.
class PackageListView(ListView):
    model = Package
    paginate_by = 20
    template_name = 'packages/package_list.html'


class PackageCreateView(CreateView):
    model = Package
    form_class = PackageCreateForm
    template_name = 'packages/package_create.html'

    def get_success_url(self):
        return '/packages/{0}'.format(self.object.basename)


class PackageView(DetailView):
    model = Package
    template_name = 'packages/package_view.html'
