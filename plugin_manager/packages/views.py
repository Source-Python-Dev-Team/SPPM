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
from ..common.helpers import get_groups
from ..users.filtersets import ForumUserFilterSet
from ..users.models import ForumUser

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
    'PackageAddContributorView',
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

    def get_context_data(self, **kwargs):
        context = super(PackageListView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page = context['page_obj']
        previous_page = (
            page.previous_page_number() if page.has_previous() else None
        )
        next_page = page.next_page_number() if page.has_next() else None
        context.update({
            'has_other_pages': page.has_other_pages(),
            'next_page': next_page,
            'previous_page': previous_page,
            'current_page': page.number,
            'total_pages': paginator.num_pages,
        })
        return context


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


class PackageAddContributorView(FilterView):
    model = ForumUser
    template_name = 'packages/contributor/add.html'
    filterset_class = ForumUserFilterSet

    def get_context_data(self, **kwargs):
        context = super(
            PackageAddContributorView, self).get_context_data(**kwargs)
        message = ''
        user = None
        if 'username' in self.request.GET:
            package = Package.objects.get(slug=self.kwargs['slug'])
            try:
                user = ForumUser.objects.get(
                    username=self.request.GET['username'])
            except ForumUser.DoesNotExist:
                pass
            else:
                if user == package.owner:
                    message = (
                        'is the owner and cannot be added as a contributor.')
                elif user in package.contributors.all():
                    message = 'is already a contributor.'
        context.update({
            'message': message,
            'user': user,
        })
        return context


class PackageAddContributorConfirmationView(FormView):
    form_class = PackageAddContributorConfirmationForm
    template_name = 'packages/contributor/add_confirmation.html'

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
            'package_requirements': self.object.package_requirements.all(),
            'pypi_requirements': self.object.pypi_requirements.all(),
            'supported_games': self.object.supported_games.all(),
            'required_in_plugins': get_groups(
                self.object.required_in_plugins.all()),
            'required_in_sub_plugins': get_groups(
                self.object.required_in_sub_plugins.all()),
            'required_in_packages': get_groups(
                self.object.required_in_packages.all()),
        })
        return context
