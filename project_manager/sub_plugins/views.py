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
from project_manager.plugins.constants import PLUGIN_PATH
from project_manager.plugins.models import Plugin
from .constants import SUB_PLUGIN_RELEASE_URL
from .forms import (
    SubPluginCreateForm, SubPluginEditForm, SubPluginSelectGamesForm,
    SubPluginUpdateForm,
)
from .mixins import RetrieveSubPluginMixin
from .models import SubPlugin, SubPluginRelease


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'SubPluginCreateView',
    'SubPluginListView',
    'SubPluginEditView',
    'SubPluginReleaseDownloadView',
    'SubPluginReleaseListView',
    'SubPluginSelectGamesView',
    'SubPluginUpdateView',
    'SubPluginView',
)


# =============================================================================
# >> VIEWS
# =============================================================================
class SubPluginListView(
    RetrieveSubPluginMixin,
    GameSpecificOrderablePaginatedListView
):
    model = SubPlugin
    orderable_columns = (
        'name',
        'basename',
    )
    orderable_columns_default = 'basename'
    paginate_by = 20
    template_name = 'sub_plugins/list.html'

    def get_queryset(self):
        return super(SubPluginListView, self).get_queryset().filter(
            plugin=self.plugin,
        ).select_related('plugin')

    def get_context_data(self, **kwargs):
        context = super(SubPluginListView, self).get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
            'paths': self.plugin.paths.all(),
            'sub_plugin_list': context['subplugin_list'],
        })
        return context


class SubPluginCreateView(
    RequirementsParserMixin, RetrieveSubPluginMixin, CreateView
):
    model = SubPlugin
    form_class = SubPluginCreateForm
    template_name = 'sub_plugins/create.html'

    @staticmethod
    def get_requirements_path(form):
        plugin_basename = form.instance.plugin.basename
        path = form.cleaned_data['path']
        basename = form.instance.basename
        return (
            f'{PLUGIN_PATH}{plugin_basename}/{path}/{basename}/'
            'requirements.ini'
        )

    def get_context_data(self, **kwargs):
        context = super(SubPluginCreateView, self).get_context_data(**kwargs)
        context.update({
            'plugin': self.plugin,
            'paths': self.plugin.paths.all()
        })
        return context

    def get_initial(self):
        initial = super(SubPluginCreateView, self).get_initial()
        initial.update({
            'plugin': self.plugin,
        })
        return initial


class SubPluginEditView(UpdateView):
    model = SubPlugin
    form_class = SubPluginEditForm
    template_name = 'sub_plugins/edit.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_initial(self):
        initial = super(SubPluginEditView, self).get_initial()
        initial.update({
            'logo': '',
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(SubPluginEditView, self).get_context_data(**kwargs)
        context.update({
            'sub_plugin': context['subplugin']
        })
        return context


class SubPluginUpdateView(
    RequirementsParserMixin, RetrieveSubPluginMixin, UpdateView
):
    model = SubPlugin
    form_class = SubPluginUpdateForm
    template_name = 'sub_plugins/update.html'
    slug_url_kwarg = 'sub_plugin_slug'

    @staticmethod
    def get_requirements_path(form):
        plugin_basename = form.instance.plugin.basename
        path = form.cleaned_data['path']
        basename = form.instance.basename
        return (
            f'{PLUGIN_PATH}{plugin_basename}/{path}/{basename}/'
            'requirements.ini'
        )

    def get_queryset(self):
        """This is to fix a MultipleObjectsReturned error."""
        return SubPlugin.objects.filter(
            pk=self.sub_plugin.pk,
        )

    def get_context_data(self, **kwargs):
        context = super(SubPluginUpdateView, self).get_context_data(**kwargs)
        sub_plugin = context['subplugin']
        context.update({
            'plugin': self.plugin,
            'sub_plugin': sub_plugin,
            'current_version': self.object.current_version,
            'paths': self.plugin.paths.all(),
        })
        return context

    def get_initial(self):
        initial = super(SubPluginUpdateView, self).get_initial()
        initial.update({
            'plugin': self.plugin,
            'version': '',
            'version_notes': '',
            'zip_file': '',
        })
        return initial


class SubPluginSelectGamesView(UpdateView):
    model = SubPlugin
    form_class = SubPluginSelectGamesForm
    template_name = 'sub_plugins/games.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_context_data(self, **kwargs):
        context = super(
            SubPluginSelectGamesView,
            self
        ).get_context_data(**kwargs)
        context.update({
            'sub_plugin': context['subplugin']
        })
        return context


class SubPluginView(RetrieveSubPluginMixin, DetailView):
    model = SubPlugin
    template_name = 'sub_plugins/view.html'
    slug_url_kwarg = 'sub_plugin_slug'

    def get_queryset(self):
        """This is to fix a MultipleObjectsReturned error."""
        return SubPlugin.objects.filter(
            pk=self.sub_plugin.pk,
        ).select_related('plugin')

    def get_context_data(self, **kwargs):
        context = super(SubPluginView, self).get_context_data(**kwargs)
        sub_plugin = context['subplugin']
        context.update({
            'sub_plugin': sub_plugin,
            'current_version': self.object.current_version,
            'contributors': self.object.contributors.all(),
            'package_requirements': self.object.package_requirements.all(),
            'pypi_requirements': self.object.pypi_requirements.all(),
            'supported_games': self.object.supported_games.all(),
        })
        return context


class SubPluginReleaseDownloadView(DownloadMixin):
    model = SubPluginRelease
    super_model = Plugin
    sub_model = SubPlugin
    slug_url_kwarg = 'sub_plugin_slug'
    super_kwarg = 'plugin'
    sub_kwarg = 'sub_plugin'
    base_url = SUB_PLUGIN_RELEASE_URL


class SubPluginReleaseListView(RetrieveSubPluginMixin, ListView):
    model = SubPluginRelease
    template_name = 'sub_plugins/releases.html'

    def get_context_data(self, **kwargs):
        context = super(
            SubPluginReleaseListView,
            self
        ).get_context_data(**kwargs)
        context.update({
            'sub_plugin': self.sub_plugin,
        })
        return context

    def get_queryset(self):
        return SubPluginRelease.objects.filter(
            sub_plugin=self.sub_plugin,
        ).order_by('-created')
