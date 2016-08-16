# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.views.generic import CreateView, DetailView, ListView, UpdateView

# App
from project_manager.common.helpers import get_groups
from project_manager.common.mixins import (
    DownloadMixin,
    RequirementsParserMixin,
)
from project_manager.common.views import OrderablePaginatedListView
from project_manager.games.mixins import GameSpecificOrderablePaginatedListView
from .constants import PACKAGE_PATH, PACKAGE_RELEASE_URL
from .forms import (
    PackageCreateForm, PackageEditForm, PackageSelectGamesForm,
    PackageUpdateForm,
)
from .mixins import RetrievePackageMixin
from .models import Package, PackageRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageCreateView',
    'PackageEditView',
    'PackageListView',
    'PackageReleaseDownloadView',
    'PackageReleaseListView',
    'PackageSelectGamesView',
    'PackageUpdateView',
    'PackageView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PackageListView(GameSpecificOrderablePaginatedListView):
    model = Package
    orderable_columns = (
        'name',
        'basename',
    )
    orderable_columns_default = 'basename'
    paginate_by = 20
    template_name = 'packages/list.html'


class PackageCreateView(RequirementsParserMixin, CreateView):
    model = Package
    form_class = PackageCreateForm
    template_name = 'packages/create.html'

    @staticmethod
    def get_requirements_path(form):
        return '{package_path}{basename}/requirements.ini'.format(
            package_path=PACKAGE_PATH,
            basename=form.instance.basename,
        )


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


class PackageUpdateView(
    RequirementsParserMixin, RetrievePackageMixin, UpdateView
):
    model = Package
    form_class = PackageUpdateForm
    template_name = 'packages/update.html'

    @staticmethod
    def get_requirements_path(form):
        return '{package_path}{basename}/requirements.ini'.format(
            package_path=PACKAGE_PATH,
            basename=form.instance.basename,
        )

    def get_context_data(self, **kwargs):
        context = super(PackageUpdateView, self).get_context_data(**kwargs)
        context.update({
            'package': self.package,
            'current_version': self.package.current_version,
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


class PackageSelectGamesView(UpdateView):
    model = Package
    form_class = PackageSelectGamesForm
    template_name = 'packages/games.html'


class PackageView(DetailView):
    model = Package
    template_name = 'packages/view.html'

    def get_context_data(self, **kwargs):
        context = super(PackageView, self).get_context_data(**kwargs)
        context.update({
            'current_version': self.object.current_version,
            'contributors': self.object.contributors.all(),
            'package_requirements': self.object.package_requirements.all(),
            'pypi_requirements': self.object.pypi_requirements.all(),
            'supported_games': self.object.supported_games.all(),
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


class PackageReleaseDownloadView(DownloadMixin):
    model = PackageRelease
    super_model = Package
    super_kwarg = 'package'
    base_url = PACKAGE_RELEASE_URL


class PackageReleaseListView(RetrievePackageMixin, ListView):
    model = PackageRelease
    template_name = 'packages/releases.html'

    def get_context_data(self, **kwargs):
        context = super(
            PackageReleaseListView,
            self
        ).get_context_data(**kwargs)
        context.update({
            'package': self.package,
        })
        return context

    def get_queryset(self):
        return PackageRelease.objects.filter(
            package=self.package,
        ).order_by('-created')
