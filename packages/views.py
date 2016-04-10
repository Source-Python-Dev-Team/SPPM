from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import Package
from .forms import PackageCreateForm, PackageUpdateForm


__all__ = (
    'PackageCreateView',
    'PackageListView',
    'PackageUpdateView',
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


class PackageUpdateView(UpdateView):
    model = Package
    form_class = PackageUpdateForm
    template_name = 'packages/package_update.html'

    def get_context_data(self, **kwargs):
        context = super(PackageUpdateView, self).get_context_data(**kwargs)
        context.update({
            'package': Package.objects.get(
                slug=context['view'].kwargs['slug'])
        })
        return context

    def get_initial(self):
        initial = super(PackageUpdateView, self).get_initial()
        initial.update({
            'version': '',
            'zip_file': '',
        })
        return initial


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
