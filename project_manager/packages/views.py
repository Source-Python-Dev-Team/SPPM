"""Package views."""

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
    """Package listing view."""

    model = Package
    orderable_columns = (
        'name',
        'basename',
    )
    orderable_columns_default = 'basename'
    paginate_by = 20
    template_name = 'packages/list.html'


class PackageCreateView(RequirementsParserMixin, CreateView):
    """Package creation view."""

    model = Package
    form_class = PackageCreateForm
    template_name = 'packages/create.html'

    def get_requirements_path(self, form):
        """Return the path for the requirements file."""
        return f'{PACKAGE_PATH}{form.instance.basename}/requirements.ini'

    def get_form_kwargs(self):
        """Add the owner to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user.forum_user
        return kwargs


class PackageEditView(UpdateView):
    """Package field editing view."""

    model = Package
    form_class = PackageEditForm
    template_name = 'packages/edit.html'

    def get_initial(self):
        """Add the logo to the initial."""
        initial = super().get_initial()
        initial.update({
            'logo': '',
        })
        return initial


class PackageUpdateView(
    RequirementsParserMixin, RetrievePackageMixin, UpdateView
):
    """Package release creation view."""

    model = Package
    form_class = PackageUpdateForm
    template_name = 'packages/update.html'

    def get_requirements_path(self, form):
        """Return the path for the requirements file."""
        return f'{PACKAGE_PATH}{form.instance.basename}/requirements.ini'

    def get_context_data(self, **kwargs):
        """Add the necessary info to the context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'package': self.package,
            'current_version': self.package.current_version,
        })
        return context

    def get_initial(self):
        """Clear out the initial."""
        initial = super().get_initial()
        initial.update({
            'version': '',
            'version_notes': '',
            'zip_file': '',
        })
        return initial


class PackageSelectGamesView(UpdateView):
    """Package Game selection view."""

    model = Package
    form_class = PackageSelectGamesForm
    template_name = 'packages/games.html'


class PackageView(DetailView):
    """Package get view."""

    model = Package
    template_name = 'packages/view.html'

    def get_context_data(self, **kwargs):
        """Add the necessary info to the context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'current_release': self.object.releases.order_by('-created')[0],
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
    """Package download view for releases."""

    model = PackageRelease
    super_model = Package
    super_kwarg = 'package'
    base_url = PACKAGE_RELEASE_URL


class PackageReleaseListView(RetrievePackageMixin, ListView):
    """PackageRelease listing view."""

    model = PackageRelease
    template_name = 'packages/releases.html'

    def get_context_data(self, **kwargs):
        """Add the package to the context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'package': self.package,
        })
        return context

    def get_queryset(self):
        """Filter down to the releases for the Package and order them."""
        return PackageRelease.objects.filter(
            package=self.package,
        ).order_by('-created')
