# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.views.generic import CreateView, DetailView, ListView, UpdateView

# App
from project_manager.common.mixins import (
    DownloadMixin,
    RequirementsParserMixin,
)
from project_manager.common.views import OrderablePaginatedListView
from project_manager.games.mixins import GameSpecificOrderablePaginatedListView
from .constants import PLUGIN_PATH, PLUGIN_RELEASE_URL
from .forms import (
    PluginCreateForm, PluginEditForm, PluginSelectGamesForm, PluginUpdateForm,
)
from .mixins import RetrievePluginMixin
from .models import Plugin, PluginRelease


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
)


# =============================================================================
# >> VIEWS
# =============================================================================
class PluginListView(GameSpecificOrderablePaginatedListView):
    model = Plugin
    orderable_columns = (
        'name',
        'basename',
    )
    orderable_columns_default = 'basename'
    paginate_by = 20
    template_name = 'plugins/list.html'


class PluginCreateView(RequirementsParserMixin, CreateView):
    model = Plugin
    form_class = PluginCreateForm
    template_name = 'plugins/create.html'

    @staticmethod
    def get_requirements_path(form):
        return '{plugin_path}{basename}/requirements.ini'.format(
            plugin_path=PLUGIN_PATH,
            basename=form.instance.basename,
        )


class PluginEditView(UpdateView):
    model = Plugin
    form_class = PluginEditForm
    template_name = 'plugins/edit.html'

    def get_initial(self):
        initial = super(PluginEditView, self).get_initial()
        initial.update({
            'logo': '',
        })
        return initial


class PluginUpdateView(
    RequirementsParserMixin, RetrievePluginMixin, UpdateView
):
    model = Plugin
    form_class = PluginUpdateForm
    template_name = 'plugins/update.html'

    @staticmethod
    def get_requirements_path(form):
        return '{plugin_path}{basename}/requirements.ini'.format(
            plugin_path=PLUGIN_PATH,
            basename=form.instance.basename,
        )

    def get_context_data(self, **kwargs):
        context = super(PluginUpdateView, self).get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
            'current_version': self.plugin.current_version,
        })
        return context

    def get_initial(self):
        initial = super(PluginUpdateView, self).get_initial()
        initial.update({
            'version': '',
            'version_notes': '',
            'zip_file': '',
        })
        return initial


class PluginSelectGamesView(UpdateView):
    model = Plugin
    form_class = PluginSelectGamesForm
    template_name = 'plugins/games.html'


class PluginView(DetailView):
    model = Plugin
    template_name = 'plugins/view.html'

    def get_context_data(self, **kwargs):
        context = super(PluginView, self).get_context_data(**kwargs)
        context.update({
            'current_version': self.object.current_version,
            'contributors': self.object.contributors.all(),
            'paths': self.object.paths.all(),
            'package_requirements': self.object.package_requirements.all(),
            'pypi_requirements': self.object.pypi_requirements.all(),
            'supported_games': self.object.supported_games.all(),
        })
        return context


class PluginReleaseDownloadView(DownloadMixin):
    model = PluginRelease
    super_model = Plugin
    super_kwarg = 'plugin'
    base_url = PLUGIN_RELEASE_URL


class PluginReleaseListView(RetrievePluginMixin, ListView):
    model = PluginRelease
    template_name = 'plugins/releases.html'

    def get_context_data(self, **kwargs):
        context = super(PluginReleaseListView, self).get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
        })
        return context

    def get_queryset(self):
        return PluginRelease.objects.filter(
            plugin=self.plugin,
        ).order_by('-created')
