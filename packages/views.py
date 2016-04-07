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
        return self.object.get_absolute_url()


class PackageView(DetailView):
    model = Package
    template_name = 'packages/package_view.html'

    def get_context_data(self, **kwargs):
        context = super(PackageView, self).get_context_data(**kwargs)
        context.update({
            'contributors': self.object.contributors.all(),
            'required_in_plugins': self.object.required_in_plugins.all(),
            'required_in_sub_plugins': self.object.required_in_sub_plugins.all(),
            'required_in_packages': self.object.required_in_packages.all(),
        })
        return context
