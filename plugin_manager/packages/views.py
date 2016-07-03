# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.db.models import F
from django.http import Http404, HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.views.generic import (
    CreateView, DetailView, FormView, UpdateView, View,
)

# 3rd-Party Django
from django_filters.views import FilterView

# App
from .constants import PACKAGE_RELEASE_URL
from .forms import (
    PackageAddContributorConfirmationForm, PackageCreateForm, PackageEditForm,
    PackageUpdateForm,
)
from .models import Package, PackageRelease
from ..common.helpers import get_groups
from ..common.views import OrderablePaginatedListView
from ..users.filtersets import ForumUserFilterSet
from ..users.models import ForumUser


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAddContributorConfirmationView',
    'PackageAddContributorView',
    'PackageCreateView',
    'PackageEditView',
    'PackageListView',
    'PackageReleaseDownloadView',
    'PackageUpdateView',
    'PackageView',
)


# =============================================================================
# >> VIEW CLASSES
# =============================================================================
class PackageListView(OrderablePaginatedListView):
    model = Package
    orderable_columns = (
        'name',
        'basename',
    )
    orderable_columns_default = 'basename'
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
            PackageAddContributorConfirmationView,
            self,
        ).get_context_data(**kwargs)
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
        package = Package.objects.get(slug=context['view'].kwargs['slug'])
        current_release = PackageRelease.objects.filter(
            package=package,
        ).order_by('-created')[0]
        context.update({
            'package': package,
            'current_release': current_release,
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
        current_release = PackageRelease.objects.filter(
            package=context['package'],
        ).order_by('-created')[0]
        context.update({
            'current_release': current_release,
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


class PackageReleaseDownloadView(View):
    model = PackageRelease
    full_path = None

    def dispatch(self, request, *args, **kwargs):
        self.full_path = (
            settings.MEDIA_ROOT / PACKAGE_RELEASE_URL / kwargs['slug'] /
            kwargs['zip_file']
        )
        if not self.full_path.isfile():
            raise Http404
        return super(
            PackageReleaseDownloadView,
            self
        ).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        zip_file = kwargs['zip_file']
        with self.full_path.open('rb') as open_file:
            response = HttpResponse(
                content=open_file.read(),
                content_type='application/force-download',
            )
        response['Content-Disposition'] = (
            'attachment: filename={filename}'.format(
                filename=zip_file,
            )
        )
        package = Package.objects.get(slug=kwargs['slug'])
        version = zip_file.split(
            '{slug}-v'.format(slug=package.slug), 1
        )[1].rsplit('.', 1)[0]
        PackageRelease.objects.filter(
            package=package,
            version=version
        ).update(
            download_count=F('download_count') + 1
        )
        return response
