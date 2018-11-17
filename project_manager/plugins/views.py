"""Plugin views."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

# App
from project_manager.common.mixins import DownloadMixin
from project_manager.games.mixins import GameSpecificOrderablePaginatedListView
from project_manager.plugins.constants import PLUGIN_PATH, PLUGIN_RELEASE_URL
from project_manager.plugins.forms import (
    PluginCreateForm,
    PluginEditForm,
    PluginSelectGamesForm,
    PluginUpdateForm,
    SubPluginPathCreateForm,
    SubPluginPathEditForm,
)
from project_manager.plugins.mixins import RetrievePluginMixin
from project_manager.plugins.models import Plugin, PluginRelease, SubPluginPath


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginCreateView',
    'PluginEditView',
    'PluginListView',
    'PluginReleaseDownloadView',
    'PluginReleaseListView',
    'PluginSelectGamesView',
    'PluginUpdateView',
    'PluginView',
    'SubPluginPathCreateView',
    'SubPluginPathDeleteView',
    'SubPluginPathEditView',
    'SubPluginPathListView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PluginListView(GameSpecificOrderablePaginatedListView):
    """Plugin listing view."""

    model = Plugin
    orderable_columns = (
        'name',
        'basename',
    )
    orderable_columns_default = 'basename'
    paginate_by = 20
    template_name = 'plugins/list.html'


class PluginCreateView(CreateView):
    """Plugin creation view."""

    model = Plugin
    form_class = PluginCreateForm
    template_name = 'plugins/create.html'

    def get_requirements_path(self, form):
        """Return the path for the requirements file."""
        return f'{PLUGIN_PATH}{form.instance.basename}/requirements.ini'

    def get_form_kwargs(self):
        """Add the owner to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user.forum_user
        return kwargs


class PluginEditView(UpdateView):
    """Plugin field editing view."""

    model = Plugin
    form_class = PluginEditForm
    template_name = 'plugins/edit.html'

    def get_initial(self):
        """Add the logo to the initial."""
        initial = super().get_initial()
        initial.update({
            'logo': '',
        })
        return initial


class PluginUpdateView(RetrievePluginMixin, UpdateView):
    """Plugin release creation view."""

    model = Plugin
    form_class = PluginUpdateForm
    template_name = 'plugins/update.html'

    def get_requirements_path(self, form):
        """Return the path for the requirements file."""
        return f'{PLUGIN_PATH}{form.instance.basename}/requirements.ini'

    def get_context_data(self, **kwargs):
        """Add the necessary info to the context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
            'current_version': self.plugin.current_version,
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


class PluginSelectGamesView(UpdateView):
    """Plugin Game selection view."""

    model = Plugin
    form_class = PluginSelectGamesForm
    template_name = 'plugins/games.html'


class PluginView(DetailView):
    """Plugin get view."""

    model = Plugin
    template_name = 'plugins/view.html'

    def get_context_data(self, **kwargs):
        """Add the necessary info to the context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'current_release': self.object.releases.order_by('-created')[0],
            'contributors': self.object.contributors.all(),
            'paths': self.object.paths.all(),
            'package_requirements': self.object.package_requirements.all(),
            'pypi_requirements': self.object.pypi_requirements.all(),
            'supported_games': self.object.supported_games.all(),
        })
        return context


class PluginReleaseDownloadView(DownloadMixin):
    """Plugin download view for releases."""

    model = PluginRelease
    super_model = Plugin
    super_kwarg = 'plugin'
    base_url = PLUGIN_RELEASE_URL


class PluginReleaseListView(RetrievePluginMixin, ListView):
    """PluginRelease listing view."""

    model = PluginRelease
    template_name = 'plugins/releases.html'

    def get_context_data(self, **kwargs):
        """Add the plugin to the context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
        })
        return context

    def get_queryset(self):
        """Filter down to the releases for the Plugin and order them."""
        return PluginRelease.objects.filter(
            plugin=self.plugin,
        ).order_by('-created')


class SubPluginPathListView(RetrievePluginMixin, ListView):
    """SubPluginPath listing view."""

    model = SubPluginPath
    template_name = 'plugins/paths/list.html'

    def get_context_data(self, **kwargs):
        """Add the plugin to the context for the template."""
        context = super().get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
        })
        return context

    def get_queryset(self):
        """Filter down to SubPluginPaths for the given plugin."""
        return super().get_queryset().filter(
            plugin=self.plugin,
        )


class SubPluginPathCreateView(RetrievePluginMixin, CreateView):
    """SubPluginPath creation view."""

    model = SubPluginPath
    form_class = SubPluginPathCreateForm
    template_name = 'plugins/paths/create.html'

    def get_initial(self):
        """Add the plugin to the initial."""
        initial = super().get_initial()
        initial.update({
            'plugin': self.plugin,
        })
        return initial


class SubPluginPathEditView(RetrievePluginMixin, UpdateView):
    """SubPluginPath update view."""

    model = SubPluginPath
    form_class = SubPluginPathEditForm
    template_name = 'plugins/paths/edit.html'
    pk_url_kwarg = 'path_pk'

    def get_context_data(self, **kwargs):
        """Add the plugin to the context for the template."""
        context = super().get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
        })
        return context


class SubPluginPathDeleteView(DeleteView):
    """SubPluginPath deletion view."""

    model = SubPluginPath

    def get_object(self, queryset=None):
        """Return the object for the view."""
        return SubPluginPath.objects.get(pk=self.kwargs.get('path_pk'))
