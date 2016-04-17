# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.shortcuts import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

# 3rd-Party Django
from django_filters.views import FilterView

# Project Imports
from users.filtersets import ForumUserFilterSet
from users.models import ForumUser

# App Imports
from .forms import (
    PackageAddContributorConfirmationForm,
    PackageCreateForm,
    PackageEditForm,
    PackageUpdateForm,
)
from .models import Package


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAddContributorConfirmationView',
    'PackageAddContributorsView',
    'PackageCreateView',
    'PackageEditView',
    'PackageListView',
    'PackageUpdateView',
    'PackageView',
)


# =============================================================================
# >> VIEW CLASSES
# =============================================================================
class PackageListView(ListView):
    model = Package
    paginate_by = 20
    template_name = 'packages/list.html'


class PackageCreateView(CreateView):
    model = Package
    form_class = PackageCreateForm
    template_name = 'packages/create.html'


class PackageEditView(UpdateView):
    model = Package
    form_class = PackageEditForm
    template_name = 'packages/edit.html'

    def get_initial(self):
        initial = super(PackageEditView, self).get_initial()
        initial.update({
            'logo': '',
        })
        return initial


class PackageAddContributorsView(FilterView):
    model = ForumUser
    template_name = 'packages/contributors/add.html'
    filterset_class = ForumUserFilterSet


class PackageAddContributorConfirmationView(FormView):
    form_class = PackageAddContributorConfirmationForm
    template_name = 'packages/contributors/add_confirmation.html'

    def get_initial(self):
        initial = super(
            PackageAddContributorConfirmationView, self).get_initial()
        initial.update({
            'id': self.kwargs['id']
        })
        return initial

    def get_context_data(self, **kwargs):
        package = Package.objects.get(slug=self.kwargs['slug'])
        user = ForumUser.objects.get(id=self.kwargs['id'])
        message = None
        if package.owner == user:
            message = 'is the owner and cannot be added as a contributor.'
        elif user in package.contributors.all():
            message = 'is already a contributor.'
        context = super(
            PackageAddContributorConfirmationView, self).get_context_data(
            **kwargs)
        context.update({
            'username': ForumUser.objects.get(id=self.kwargs['id']).username,
            'message': message,
        })
        return context

    def form_valid(self, form):
        package = Package.objects.get(slug=self.kwargs['slug'])
        package.contributors.add(form.cleaned_data['id'])
        return HttpResponseRedirect(package.get_absolute_url())


class PackageUpdateView(UpdateView):
    model = Package
    form_class = PackageUpdateForm
    template_name = 'packages/update.html'

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
            'version_notes': '',
            'zip_file': '',
        })
        return initial


class PackageView(DetailView):
    model = Package
    template_name = 'packages/view.html'

    def get_context_data(self, **kwargs):
        context = super(PackageView, self).get_context_data(**kwargs)
        context.update({
            'contributors': self.object.contributors.all(),
            'required_in_plugins': self.object.required_in_plugins.all(),
            'required_in_sub_plugins': self.object.required_in_sub_plugins.all(),
            'required_in_packages': self.object.required_in_packages.all(),
        })
        return context
